## 获取当前账号绑定的地址

```
/api/hub/bound_addresses?local=true [GET]

Response:
    {
        "11312312": [], 
        "dfsdffsdf": [], 
        "hahahaha": [], 
        "qwerty": [
            "0x6943423caea4cc808db04ac1b643111a2b0f0de9", 
            "0xa943423caea4cc808db04ac1b643111a2b0f0de9"
        ], 
        "sfsfsf": [], 
        "zxzaa": []
    }


local 为真时
    只返回 eth.accounts中有且已绑定的地址
```

## 绑定地址：

没有指定 namespace 时会使用 default_namespace,
若 default_namespace 为空，默认绑定到个人账号

```
/api/hub/addresses [POST]

Request:
    {
      "namespace":"qwerty",
      "address":"0x4b81766d4088533e710bb6251065ab93293fb51c"
    }

Response:
    {
        "address": "0x4b81766d4088533e710bb6251065ab93293fb51c",
        "created_at": "2016-11-24T21:50:10+08:00"
    }
```

## 设置默认 namespace

```
/api/hub/default-namespace [POST]

Request:
    {"namespace":"qwerty"}
    
Response:
    "qwerty"
```

## 获取默认 namespace

```
/api/hub/default-namespace [GET]

Response:
    "qwerty"
```