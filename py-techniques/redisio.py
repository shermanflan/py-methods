import redis

conn = redis.Redis(
        host='[server].redis.cache.windows.net',
        port=6380,
        password='[secret]',
        ssl=True)

conn.set('secret', 'ni!')
print(conn.get('secret'))

# Sets iff key does not exist
conn.setnx('secret', 'icky-icky-icky-ptang-zoop-boing!')
print(conn.get('secret'))

# Gets and sets
print(conn.getset('secret', 'icky-icky-icky-ptang-zoop-boing!'))

print(conn.get('secret'))

# Get a substring
print(conn.getrange('secret', -6, -1))

# Replace a substring
conn.setrange('secret', 0, 'ICKY')

print(conn.get('secret'))

# Set multiple keys at once
conn.mset({'pie': 'cherry', 'cordial': 'sherry'})

# Get multiple keys
print(conn.mget(['pie', 'cordial']))

# Delete a key
conn.delete('pie')

# Increment
conn.set('carats', 24)

conn.incr('carats')
conn.incr('carats', 10)
conn.decr('carats')
conn.decr('carats', 15)

print(conn.get('carats'))

conn.set('fever', '101.5')

conn.incrbyfloat('fever')
conn.incrbyfloat('fever', 0.5)

print(conn.get('fever'))

# Lists (only strings)
conn.lpush('zoo', 'bear')
conn.lpush('zoo', 'alligator', 'duck')
conn.linsert('zoo', 'before', 'bear', 'beaver')
conn.linsert('zoo', 'after', 'bear', 'cassowary')
conn.lset('zoo', 2, 'marmoset') # offset
conn.rpush('zoo', 'yak') # end

print(conn.lindex('zoo', 3))
print(conn.lrange('zoo', 0, 2))

conn.ltrim('zoo', 1, 4) # keep range
print(conn.lrange('zoo', 0, -1)) # get all

# Hashes
conn.hmset('song', {'do': 'a deer', 're': 'about a deer'})
conn.hset('song', 'mi', 'a note to follow re')

print(conn.hget('song', 'mi'))
print(conn.hmget('song', 're', 'do'))

print(conn.hkeys('song'))
print(conn.hvals('song'))
print(conn.hlen('song'))

# Set if doesn't exist
conn.hsetnx('song', 'fa', 'a note that rhymes with la')

print(conn.hgetall('song'))

# Sets
conn.sadd('zoo2', 'duck')
conn.sadd('zoo2', 'bird')
conn.sadd('zoo2', 'dog')

print(conn.scard('zoo2'))
print(conn.smembers('zoo2'))

conn.srem('zoo2', 'dog') # remove

conn.sadd('better_zoo', 'tiger')
conn.sadd('better_zoo', 'wolf')
conn.sadd('better_zoo', 'duck')

print(conn.smembers('better_zoo'))

print(conn.sinter('zoo2', 'better_zoo'))
print(conn.sinterstore('fowl_zoo', 'zoo2', 'better_zoo')) # store in fowl_zoo

print(conn.smembers('fowl_zoo'))

conn.sunion('zoo2', 'better_zoo')
conn.sunionstore('fabulous_zoo', 'zoo2', 'better_zoo') # store

print(conn.smembers('fabulous_zoo'))

conn.sdiff('zoo2', 'better_zoo')
conn.sdiffstore('zoo_sale', 'zoo2', 'better_zoo')

print(conn.smembers('zoo_sale'))

# Sorted sets
import time

now = time.time() # epoch
print(now)

conn.zadd('logins', 'smeagol', now)
conn.zadd('logins', 'sauron', now+(5*60)) # +5 min
conn.zadd('logins', 'bilbo', now+(2*60*60)) # +2 hr
conn.zadd('logins', 'treebeard', now+(24*60*60)) # + 1 day

print(conn.zrank('logins', 'bilbo'))
print(conn.zscore('logins', 'bilbo'))
print(conn.zrange('logins', 0, -1)) # all
print(conn.zrange('logins', 0, -1, withscores=True)) # with zscores

# Bits: good for large numeric data sets
days = ['2013-02-25', '2013-02-26', '2013-02-27']
big_spender = 1089
tire_kicker = 40459
late_joiner = 550212

conn.setbit(days[0], big_spender, 1)
conn.setbit(days[0], tire_kicker, 1)
conn.setbit(days[1], big_spender, 1)
conn.setbit(days[2], big_spender, 1)
conn.setbit(days[2], late_joiner, 1)

for day in days:
    print(conn.bitcount(day)) # get visitor count

print(conn.getbit(days[1], tire_kicker)) # check

conn.bitop('and', 'everyday', *days) # bit and on days
print(conn.bitcount('everyday')) # how many visited everyday
print(conn.getbit('everyday', big_spender))

conn.bitop('or', 'alldays', *days)
print(conn.bitcount('alldays')) # get total unique users

# Cache: use the expire() function to instruct Redis how long to keep the key. 
key = 'now you see it'
conn.set(key, 'but not for long')

conn.expire(key, 5)

print(conn.ttl(key))
print(conn.get(key))

time.sleep(6)
print(conn.get(key))
