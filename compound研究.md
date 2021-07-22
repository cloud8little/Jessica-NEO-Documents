#### 存款  supply

1. ETH 其它ERC20资产

- 调用cETH.mint 将用户账户下ETH转入cETH合约地址中即可

- 有2个参数比较重要，exchangeRate 对用cETH和ETH的兑换比例 ；存款利率 supplyRatePerblock

  **exchangeRate** 

```
 oneCTokenInUnderlying = exchangeRateCurrent / (1 * 10 ^ (18 + underlyingDecimals - cTokenDecimals))
```

注意，compound目前所有cToken的精度都设置为8。

举例 ETH - cETH （8）

举例 USDT(精度6)-cUSDT(精度8)

```
1cUSDT = exchangeRateCurrent /(10^16) USDT
```

如果想知道存款账户下的cUSDT能够取出多少USDT，则用

```
underlyingTokens = cTokenAmount * oneCTokenInUnderlying
```

**supplyRatePerblock**

根据所使用的利率模型分别计算：输入：cash, totalBorrows,totalReserves, reserveFactorMantissa

cToken中的所有余额，总借款数，总储备金额，储备因子。前面两个好理解，后面两个后面细说

- 求得借款利率borrowRate(根据cash, totalBorrows,totalReserves) 在后面借款部分提到
- 求利用率U = 当总借款为0，0；否则，borrows*1e18/(cash+borrows-reserves)
- U * borrowRate * ((1e18 - reserveFactorMantissa) /1e18) / 1e18最后得到结果

求存款利率的模型基本上都是一致的。

#### 取款 supply

redeem

1. 先统计利息 怎么统计 后面说 
2. 


#### 借款-还款 borrow

首先需要充抵押物，比如抵押ETH，借出DAI

1. ETH充进cETH合约中，即cETH.mint操作，具体比如充3ETH得到多少的cETH,根据exchangeRateCurrent而定；具体exchangeRateCurrent怎么计算的，在后面讲
2. 用户调用comtroller.enterMarkets([cETH])，签上用户签名
3. 查看用户流动性如何，即用户最多可以借出多少钱。该方法将会根据用户所抵押的总额度和总借款，计算剩余的借款额度是多少 （具体怎么计算后面介绍）
4. 可借出的DAI的数量 = 流动性/DAI的价格
5. cDAI.borrow(想要借出的数量)
6. 查看当前的borrowbalance,borrowRateperblock 
7. cDAI.repayBorrow(需要换DAI的数量)

**exchangeRateCurrent**: cToken 与underlying asset 之间的兑换率怎么计算？

先计算一遍利息

1. 当前cToken池供应总量为零时，定为初始交换率initialExchangeRate
2. (cash + borrows - reserves) * 1e18 / totalSupply

**borrowRatePerBlock**

1. 找到cToken所使用的利率模型，传入cash ,borrows, reserves.

2. U = 当总借款为0，0；否则，borrows*1e18/(cash+borrows-reserves)

3. 比如jumpratemodel. 

4. U <= kink(一定值) borrowRatePerBlock = U * multiplierPerBlock / 1e18 +  baseRatePerBlock

5. U > kink(一定值) 超出部分 (U - kink) * jumpMultiplierPerBlock / 1e18 + (kink * multiplierPerBlock / 1e18 +  baseRatePerBlock)

   参数 multiplierPerBlock  jumpMultiplierPerBlock  baseRatePerBlock kink都是在定义利率模型初始生成的，可以更换cToken的利率模型，将会使得计算使用率的方式改变，进而改变借款利率

或者抵押DAI，借出ETH

**查看账户流动性** getAccountLiquidity 由comptroller调用 -> getHypotheticalAccountLiquidityInternal

尤其是当用户有存款有多笔借款的时候

- 读取账户所有的借款cToken，借款额borrowBalance， exchangeRate, cTokenBalance
- cToken在市场中设置的抵押因子collateralFactor； 目前ETH、DAI大部分资产都设置的为75%
- tokensToDenom = normalized price value = collateralFactor * exchangeRate * underlyingasset价格
- sumCollateral += tokensToDenom * cTokenBalance  抵押物的总价值
- sumBorrowsPlusEffects += underlyingasset * borrowBalance    借款总价值
- 当抵押物大于借款价值，正流动性（说明正常借款，不进入清算）：可借额度 = sumCollateral - sumBorrowsPlusEffects 
- 当抵押物小于借款价值，负流动性（说明抵押物价值不足了）

**repayBorrowAllowed** comptroller调用 

- updateCompBorrowIndex   由于流动性挖矿已经停止，
  - compBorrowState[cToken] 取deltaBlocks=最新区块-compBorrowState.block
  - compSpeeds[cToken]
  - borrowAmount = totalBorrows/marketBorrowIndex
  - compAccrued = deltaBlocks * borrowSpeed
  - borrowAmount>0, 取ratio = compAccrued *1e36/borrowAmount 否则取ratio = 0
  - 新的compBorrowState[cToken] = index: compBorrowState.index*1e36 + ratio , block:blockNumber
- distributeBorrowerComp
  - compBorrowState[cToken] 取deltaBlocks=最新区块-compBorrowState.block
  - borrowIndex = compBorrowState[cToken].index * 1e36
  - borrowerIndex = compBorrowerIndex [cToken] [borrower] * 1e36
  - compBorrowerIndex [cToken] [borrower] = borrowIndex 
  - 如果borrowerIndex>0, 
    - borrowAmount = borrowBalance/CToken.borrowIndex
    - borrowAmount * (borrowIndex - borrowerIndex)
    -  compAccured[borrower] = compAccured[borrower] + borrowAmount * (borrowIndex - borrowerIndex)

问题： compBorrowState是做什么用的？compAccured

**seizeAllowed** comptroller调用 

- 由seizeGuardianPaused控制是否暂停清算行为

- updateCompSupplyIndex（抵押物cToken）

  - deltaBlocks = 当前区块blockNumber - compSupplyState[cToken].block
  - compAccrued = deltaBlocks * compSpeeds[cToken]
  - ratio = cToken.totalSupply > 0 ? compAccrued * 1e36/cToken.totalSupply
  - index = ratio +  compSupplyState[cToken].index
  - compSupplyState[cToken] = index: index   block: 当前区块blockNumber

- distributeSupplierComp(抵押物cToken, 借款人)

  - supplyIndex = compSupplyState[cToken].index
  - supplierIndex = compSupplierIndex[cToken] [借款人]
  - compSupplierIndex[cToken] [借款人] = supplyIndex
  - 如果supplierIndex =0 而且supplyIndex>0  则supplierIndex = compInitialIndex
  - deltaIndex = supplyIndex - supplierIndex 
  - supplierTokens = 借款人的cToken余额
  - supplierDelta = supplierTokens * deltaIndex 
  - supplierAccrued = compAccrued[借款人] + supplierDelta 
  - compAccrued[借款人] = supplierAccrued 

- distributeSupplierComp(抵押物cToken, 清算人)

  - supplyIndex = compSupplyState[cToken].index
  - supplierIndex = compSupplierIndex[cToken] [清算人]
  - compSupplierIndex[cToken] [清算人] = supplyIndex
  - 如果supplierIndex =0 而且supplyIndex>0  则supplierIndex = compInitialIndex
  - supplierAccrued = compAccrued[清算人] + 清算人的cToken余额 * compSupplyState[cToken].index - compSupplierIndex[cToken] [清算人]
  - compAccrued[清算人] = supplierAccrued 

  问题：compSpeeds在哪里设置？只要compSpeeds有值了，其它就都有值了 compAccrued有什么用？

  comptroller可以通过_setCompSpeed 设置某一个cToken的compSpeed,即对应每个市场所能分到的COMP比例

  claimComp: 

  

**getAccountSnapshot** 重点观察

返回账户的cToken余额，借款余额，兑换率



**累加利息**   **accureInterest**

- 利息因子 = borrowRate * blockDelta = r * t

- 累加利息 interestAccumulated = borrowRate * blockDelta * totalBorrows 

- totalReserves = 之前储备总值 +  reserveFactor * 累加利息

- borrowIndex = borrowRate * blockDelta * borrowIndex + borrowIndex = borrowIndex * (1 + 利息因子 ) 

初始化cToken时，borrowIndex = 1



**借款总额**  **borrowBalanceStored**

1. 账户的借款额* market.borrowIndex / borrower.borrowIndex

有两个借款因子，最新的市场借款因子是全局的，还有一个是借款人在借款发生的区块时候的借款因子



**取款** 对应存款

有两种方式：第一种可以选择取回多少cToken，第二种可以选择取回多少原来的资产Token（以什么结算？）

- redeem() 
- redeemUnderlying()
  - **redeemAllowed**  调用 **getHypotheticalAccountLiquidityInternal**
  - 


**还款**

**什么时候可以进行清算**

**liquidateBorrow** 调用 

- liquidateBorrowAllowed  

​            getAccountLiquidityInternal  查看用户的抵押金额是否小于借款的金额

​            closeFactorMantissa comptroller来设置的，清算百分比

- repayBorrowFresh

  - repayBorrowAllowed
    - updateCompBorrowIndex
    - distributeBorrowerComp

- liquidateCalculateSeizeTokens 怎么计算的

  1. 借出去的underlyingtoken的Oracle价格
  2. 抵押物的underlyingtoken的Oracle价格
  3. 两者价格都不能为零
  4. 抵押物cToken的exchangeRate
  5. 可以清算的抵押物Token数量  = actualRepayAmount * (liquidationIncentive * priceBorrowed) / (priceCollateral * exchangeRate)
  
  - liquidationIncentiveMantissa comptroller需要设置 比如链上是1.08左右的数值，即以92的折扣
  
- seize 怎么计算 由抵押物cToken调用
  
- seizeAllowed 由comptroller调用
  
  - borrower借款人的cToken余额 - seizeTokens
- 清算人账户cToken余额加上seizeTokens
  - 相当于借款人发送了seizeTokens个cToken给清算人
  
  
  
  
  
  
  
  





