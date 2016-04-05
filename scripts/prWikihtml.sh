echo enter usrname for twiki
read username
echo enter pass for twiki
read password

echo start creating login...

echo key A > login_script
echo key Down Arrow >>  login_script
echo key Down Arrow >> login_script
echo key Down Arrow >> login_script
echo key Up Arrow >> login_script

a=$username
b=${#a}
let b=$b-1
for i in `seq 0 $b`; 
do
  echo key ${a:$i:1} >> login_script
done

echo key Down Arrow >> login_script
echo key Down Arrow >> login_script
echo key Down Arrow >> login_script
echo key Down Arrow >> login_script
echo key Down Arrow >> login_script

a=$password
b=${#a}
let b=$b-1
for i in `seq 0 $b`; 
do
  echo key ${a:$i:1} >> login_script
done

echo key Down Arrow >> login_script
echo key Down Arrow >> login_script
echo key ^J  >> login_script      
echo key \\   >> login_script
echo key P   >> login_script
echo key ^J  >> login_script
echo key ^J  >> login_script
echo key \\   >> login_script
echo key Q   >> login_script

if [ -f ./LVNAffectingChangesTable ];
then
  rm LVNAffectingChangesTable
fi
lynx -cmd_script=login_script http://viini.dev.salab.noklab.net/twiki/bin/view/SA/LVNAffectingChangesTable
mv LVNAffectingChangesTable LVN.html
chmod 777 LVN.html
rm login_script
