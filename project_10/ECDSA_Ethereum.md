# Application of this deduce technique in Ethereum with ECDSA

## **ECDSA**

椭圆曲线数字签名算法 (ECDSA) 是一种用于创建和验证数字签名的加密算法。它基于椭圆曲线的数学原理，用于许多安全和身份验证很重要的应用中，例如银行业、电子商务和数字身份系统。

ECDSA 的工作原理是使用私钥生成消息签名，并使用相应的公钥来验证签名。私钥是保密的，公钥可以公开共享。当使用私钥对消息进行签名时，生成的签名对于该消息以及用于对其进行签名的私钥来说是唯一的。

为了验证签名，消息的接收者使用公钥来验证签名。如果签名有效，则接收者可以确定该消息是由私钥所有者发送的。

ECDSA 被广泛使用，因为它提供了强大的安全性，同时需要相对较少的计算能力。它被认为是当今最安全的签名方案之一，并广泛应用于现代密码学中

ECDSA 使用有限域上椭圆曲线的代数结构。大多数区块链使用的常量都是在[secp256k1 标准](http://www.secg.org/sec2-v2.pdf?ref=hackernoon.com)中设置的。

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_10/%E6%A4%AD%E5%9C%86%E6%9B%B2%E7%BA%BF%E7%9A%84%E7%A4%BA%E4%BE%8B%E5%BD%A2%E7%8A%B6.jpg)

在区块链出现之前，这种椭圆曲线标准根本不常见。事实上，大多数主流硬件厂商都不支持该曲线的硬件加密。有传言称，之所以选择 secp256k1，是因为它被 NSA 植入盗窃后门)的可能性最小。

## **ECDSA实现**

**签名过程：**

1.  选择一条椭圆曲线Ep(a, b)和基点G。
2.  选择私钥k（k < n），其中n是基点G的阶数，通过计算公钥K = kG。
3.  生成随机数r（r < n），计算点R = rG。
4.  将原数据和点R的坐标值x、y作为参数，计算哈希值Hash = Hash(原数据, x, y)（通常使用哈希函数）。
5.  计算s ≡ r - Hash * k (mod n)。
6.  如果r或s中有一个为0，则重新从步骤3开始执行。

**验证过程：**

1.  接收方在收到消息m和签名值(r, s)后进行以下运算。
2.  计算sG + H(m)P = (x1, y1)，其中H(m)是对消息m进行哈希计算的结果。
3.  验证等式：r1 ≡ x1 (mod n)，其中r1为计算得到的临时值。
4.  如果等式成立，则接受签名；否则，签名无效。



## **签名如何运作**
![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_10/%E7%AD%BE%E5%90%8D%E8%BF%90%E4%BD%9C.jpg)
在区块链系统中，任何密钥持有者都可以使用其私钥来签署数据。这会产生签名。获得签名的人可以使用它来：

1. 恢复作者的公钥（账户地址）
2. 验证消息是否与作者签名的消息相同

智能合约和以太坊客户端都能够验证 ECDSA 签名。智能合约中的 ECDSA 验证允许区块链之外的防篡改通信。

## ECDSA 在以太坊中的使用

在以太坊中，ECDSA 被用作创建和验证数字签名以进行交易认证的算法。以太坊交易使用 ECDSA 算法用发送者的私钥进行签名，签名包含在交易数据中。

当交易被广播到网络时，网络上的节点使用 ECDSA 算法来使用发送者的公钥来验证签名。如果签名有效，则交易被视为经过身份验证，并且可以添加到区块链中。

ECDSA 还用于以太坊中的密钥管理，其中生成公钥-私钥对并用于验证交易和签署消息。此外，以太坊中的智能合约可以将 ECDSA 用于需要安全身份验证和数字签名的各种应用程序。



参考资料：

https://blog.coinfabrik.com/wp-content/uploads/2016/06/ECDSA-Security-in-Bitcoin-and-Ethereum-a-Research-Survey.pdf

https://dev.to/yusuferdogan/the-elliptic-curve-digital-signature-algorithm-ecdsa-jng
