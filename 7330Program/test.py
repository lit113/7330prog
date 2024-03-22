a = [' 45678901', ' Jack Doe', ' 20101231', ' 200', ' BC']
b = []
for e in a:
    ee = e.strip()
    b.append(ee)
print([x.strip() for x in a])
