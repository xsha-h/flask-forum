from exts import cache


# 设置redis键值对
def set(key, value, timeout=60):
    return cache.set(key, value, timeout)


# 获取redis键对应的值
def get(key):
    return cache.get(key)


# 删除redis的键和值
def delete(key):
    return cache.delete(key)
