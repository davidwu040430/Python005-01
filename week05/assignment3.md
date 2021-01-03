1. 淘宝购物/结账，引入rabbitmq，主要解决的是：1、异步 2、解偶 3、消息可以持久化 4、流量削峰
2. 避免消息重复投递或重复消费，核心是要求，消费所引起的业务操作要设计成幂等性
3. fanout是不处理路由键，一个发送到交换机的消息，都会复制到所有绑定了这个交换机的队列。direct处理路由键，要求路由键完全匹配的消息才会转发到这个队列里。topic处理路由键，而且是跟某种模式匹配，此时队列需要绑定一个模式，譬如#/*。
4. 架构中引入消息队列，总体来讲利大于弊。缺点：1、逻辑被异步了，以前逻辑是放在一起的，处理是显式的，但是用了消息机制：逻辑被隐藏起来了，大家只看到发出了消息，有哪些系统收到了消息，处理了消息，对于发送消息的系统是不可见的。排查错误的时候也会很困难。