### This is an overview of fee for N3 network. 
Default there will be 21 committee member.

| Action                                                       | Fee      |
| ------------------------------------------------------------ | -------- |
| send neo                                                     | 0.07 gas    |
| send gas                                                     | 0.08 gas     |
| deploy contract                                              | 10.12 gas  |
| update contract                                              | 3 gas      |
| register candidate                                           | 1000.01 gas |
| vote candidate                                               | 0.03 gas    |
| vote for committee benefits/pool/day | 822.86 gas  |
| vote for cn node benefits/pool/day  | 1,645.72 gas |
| committee benefits/day                                       | 137.15 gas  |
| every 100 neo holder benefits /day                           | 0.00288 gas  |
| set information for committee member                         | 1.5 gas     |


        ContractManagement  0xfffdc93764dbaddd97c48f252a53ea4643faa3fd
        StdLib              0xacce6fd80d44e1796aa0c2c625e9e4e0ce39efc0
        CryptoLib           0x726cb6e0cd8628a1350a611384688911ab75f51b
        LedgerContract      0xda65b600f7124ce6c79950c1772a36403104f2be
        NeoToken            0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5
        GasToken            0xd2a4cff31913016155e38e474a2c06d08be276cf
        PolicyContract      0xcc5e4edd9f5f8dba8bb65734541df7a1c081c67b
        RoleManagement      0x49cf4e5378ffcd4dec034fd98a174c5491e395e2
        OracleContract      0xfe924b7cfe89ddd271abaf7210a80a7e11178758


### Governance

- ONly committee reward with CASH, NEO holder reward and Vote reward is in unclaimed balance account.
- 只有委员会成员激励以现金GAS发放，NEO持有者奖励以及投票奖励都将进入unclaimed账户，需要发送一笔交易将其自动claim出来
- If change votes in the committeemember * N th block, and vote to non-committee member, no reward. 



