while read p; do
  echo $p
  if [[ $p =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
    sudo openssl s_client -connect $p -ciper ECDHE-RSA-AES128-GCM-SHA256 | grep Protocol
  else
    echo $p
  fi
done < master.txt
