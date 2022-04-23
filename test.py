import subprocess



lines=subprocess.check_output ("ifconfig", stderr=open('/dev/null','w'))
print(lines)

for line in lines.splitlines():
    line_content=line.split()
    print(line_content[0] )
    # if line_content[0] =='UID':