## Project17：比较Firefox和谷歌的记住密码插件的实现区别

### **一、Password**

Password 是 Web 服务主要的认证方式之一。

Password 一般以 Hash 后的形式存储在数据库中。这些数据库如果被拖库，使用 Dictionary Attack 可以轻松破解，因为他们的熵很低。相同的密码会被不同的用户使用或同一个用户在不同系统中使用。

为了解决这个问题，设计者在密码 Hash 的过程里加入了 _salt_。

> **Dictionary Attack** 一个字典文件，储存了单词、短语、常用密码和他们 hash 后结果。将密码与 hash 结果对比，就能破解。  
>
> **Brute Force Attack** 尝试每一个给定长度下的字符组合，效率很低。

加盐已经可以解决大部分问题，但无法阻止 Brute Force Attack，借助 GPU、FPGA、ASIC 等定制硬件可以非常低成本的进行 Hash 计算。此外，如果 salt 和 password 被一起被拖库（甚至代码），会使得破解成本更加低。

这里核心的问题是，Hash 方法使用的是无内存计算的，而 GPU、ASIC 等硬件可以让无内存计算变得非常高效。但是，当一个 Hash 方法需要用到一大块内存去计算的时候，这些硬件就会束手无策。所以 memory-hard hash function 开始被设计和使用。

Memory-hard hash function 也可以被用在加密货币的工作量证明中，用来压制 GPU 和 ASIC 在加密货币中的滥用。例如 scrypt 被用作莱特币的工作量证明算法。
**其中，火狐浏览器使用PBKDF2，谷歌浏览器使用Argon2**

### 二、Argon2d


**Argon2d**使用依赖数据的内存访问，这使得它很适合用于加密数字货币和工作量证明的应用程序，而不会受到侧信道定时攻击的威胁。**Argon2i** 使用与数据无关的内存访问，这是密码哈希的首选方法。**Argon2id** 在内存第一次迭代的前半部分充当 Argon2i，其余部分则充当 Argon2d。因此，基于时间 —— 空间的平衡，它既提供了侧信道攻击保护也节约了暴力开销。Argon2i 对内存进行了更多的传递，以防止权衡攻击的发生。


![](https://github.com/happyhippo111/No.61-/blob/main/project_17/P1.png)


### Argon2安全性分析

该协议旨在具有两个主要的安全属性：

-   “被动”攻击者（可以读取服务器存储的数据库内容）可以做两件事：1：学习kA。2：对密码执行“硬”暴力攻击，其中“硬”意味着他们必须为每个密码猜测执行 64K/8/1-scrypt。
-   “活跃”攻击者（可以窃听TLS连接，或者破坏正在运行的密钥服务器，从而可以观察发送到/来自客户端的消息）可以做三件事。1：学习kA。2：控制帐户（即生成断言）。3：对密码（以及kB）执行“简单”的暴力攻击，其中“简单”意味着他们必须对要测试的每个猜测的密码进行1000轮PBKDF。

这比早期基于SRP的协议弱，但仍然比常见的行业实践更强，并且客户更容易实现。特别是，客户端不需要执行基于 scrypt 的拉伸或 SRP。

与基于 SRP 的协议一样，如果客户端是在 Web 内容中实现的，那么强大的主动攻击者（可以 MitM TLS 连接，从而提供篡改的客户端代码）可以绕过整个协议并直接学习密码。当然，这包括决定（或被迫）提供此类页面的服务器。

长期服务器数据旨在防止“简单”字典攻击，这意味着给定存储在数据库中的所有内容，被动攻击者仍必须执行完整的 scrypt 延伸以测试每个密码猜测。

被动攻击者可以访问用作密码猜测预言机的两个值。第一个是“verifyHash”，它派生自完整的基于 scrypt 的延伸的输出。第二个是（可以与一些B类加密数据结合使用来测试密码），它也受到scrypt步骤的保护：对于每个密码，攻击者运行完整的计算以得出kB，然后尝试解密一些数据并查看其HMAC检查是否通过。`wrap(wrap(kB))`

存储的预加密响应也将用作预言机，但服务器明确不保留加密它的响应。由于keyFetchToken是随机生成的，并且独立于用户的密码，因此它加密的数据无助于测试密码猜测。`GET /account/keys``keyFetchToken`

### PBKDF2
![](https://github.com/happyhippo111/No.61-/blob/main/project_17/P2.png)
初始的密码跟salt经过PRF的操作生成了一个key，然后这个key作为下一次加密的输入和密码再次经过PRF操作，生成了后续的key，这样重复很多次，生成的key再做异或操作，生成了最终的T，然后把这些最终生成的T合并，生成最终的密码。

根据2000年的建议，一般来说这个遍历次数要达到1000次以上，才算是安全的。当然这个次数也会随着CPU计算能力的加强发生变化。这个次数可以根据安全性的要求自行调整。

有了遍历之后，为什么还需要加上salt呢？加上salt是为了防止对密码进行彩虹表攻击。也就是说攻击者不能预选计算好特定密码的hash值，因为不能提前预测，所以安全性得以提高。标准salt的长度推荐是64bits，美国国家标准与技术研究所推荐的salt长度是128 bits。
### Argon2实现方式

所需架包

```
<dependency>
		<groupId>de.mkammerer</groupId>
		<artifactId>argon2-jvm</artifactId>
		<version>2.4</version>
</dependency>
```

代码工具类

```
import org.springframework.security.crypto.password.PasswordEncoder;
import de.mkammerer.argon2.Argon2;
import de.mkammerer.argon2.Argon2Factory;

public class Argon2PasswordEncoder implements PasswordEncoder {
    private static final Argon2 ARGON2 = Argon2Factory.create();

    private static final int ITERATIONS = 2;
    private static final int MEMORY= 65536;
    private static final int PARALLELISM = 1;

    @Override
    public String encode(CharSequence rawPassword) {
        final String hash = ARGON2.hash(ITERATIONS, MEMORY, PARALLELISM, rawPassword.toString());
        return hash;
    }

    @Override
    public boolean matches(CharSequence rawPassword, String encodedPassword) {
        return ARGON2.verify(encodedPassword, rawPassword.toString());
    }

    public static void main(String[] args){
        PasswordEncoder passwordEncoder=new Argon2PasswordEncoder();
        String hashedPassword=passwordEncoder.encode("123456");
        System.out.println(hashedPassword);
    }

}
```


**参考文献**
>  https://github.com/mozilla/fxa-auth-server/wiki/onepw-protocol#vs-old-sync
> [使用Argon2进行加解密_argon.verify_傲慢小胖妞的博客-CSDN博客](https://blog.csdn.net/weixin_42932323/article/details/109984821)
