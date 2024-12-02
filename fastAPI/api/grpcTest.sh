grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 list poker5cd.Poker5cdService
#grpcurl -plaintext localhost:50051 list poker5cd.Poker5cdService.Hello
#grpcurl -plaintext localhost:50051 list poker5cd.Poker5cdService.HelloAgain
grpcurl -plaintext -d '{"name":"adam", "uid":"oA0f" }' localhost:50051 poker5cd.Poker5cdService/Hello
grpcurl -plaintext -d '{"name":"Elza", "uid":"x111"}' localhost:50051 poker5cd.Poker5cdService/HelloAgain