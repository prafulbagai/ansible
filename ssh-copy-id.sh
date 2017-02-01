for line in $(cat servers.txt);
do
	OIFS=$IFS
	IFS='='
	pair=($line)
	ip=${pair[0]}
	passwd=${pair[1]}
	ssh -oStrictHostKeyChecking=no -oPasswordAuthentication=no $h root@$ip "exit"
	sshpass -p $passwd ssh-copy-id root@$ip
	IFS=$OIFS
done