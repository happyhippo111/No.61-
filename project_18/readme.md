比特币测试币（Testnet）是一个由比特币社区维护的测试网络，它使用不同的区块链和比特币地址前缀，以便与真实网络区分。Testnet上的测试币是有价值的，但是它们没有实际的货币价值，可以在测试网络中的水龙头获得。<br>

访问的[Bitaddress网址](https://www.bitaddress.org/bitaddress.org-v3.3.0-SHA256-dec17c07685e1870960903d8f58090475b25af946fe95a734f88408cef4aa194.html?testnet=true)，在网站上随机移动鼠标，进度到100%来生成测试币地址。要设置testnet=true这项，才能生成m或其他开头的testnet测试币地址；如果没有设置，那么生成的地址会以1开头，这是正式的比特币地址。

记录图中出现的地址和私钥：

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_18/%E6%B5%8B%E8%AF%95%E7%89%88%E5%9C%B0%E5%9D%80.png)

登录比特币的测试币水龙头，获取一定数量的测试用币

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_18/%E8%8E%B7%E5%8F%96%E6%B5%8B%E8%AF%95%E5%B8%81.png)

在这里可以看到这笔交易的收款方地址（我的地址）,以及本次交易的tx。

进入网站https://live.blockcypher.com/，查询我的账户交易信息和刚刚的交易记录

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_18/%E8%B4%A6%E6%88%B7%E8%AE%B0%E5%BD%95.png)

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_18/%E4%BA%A4%E6%98%93%E4%BF%A1%E6%81%AF.png)

使用python自写脚本，可以解析获取该交易的详细信息，脚本运行结果如下：

![Alt text](https://github.com/happyhippo111/No.61-/blob/main/project_18/%E8%84%9A%E6%9C%AC%E8%BF%90%E8%A1%8C%E7%BB%93%E6%9E%9C.png)

完整爬取内容请见文件夹内parsed tx data.md文件

在tx里面可以看到交易的地址、id、哈希值，交易时间、交易金额、是否双花等信息







