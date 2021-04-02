#!/bin/sh

#bash script to automate picture capturing for database
#FOLLOWING SCRIPT REQUIRES FSWEBCAM TO BE INSTALLED

echo -n "Please specify existing file path to save pictures in: "
while true
do
read location
location+="/"
if [ ! -d "$location" ]
then
 echo -n "Patho does not exist, re-enter or press ^C to exit: "
else
break
fi
done
echo -n "Enter number of people taking pictures: "
read NPeople
echo -n "Specify number of pictures to be taken per person: "
read NPictures

for (( j=1 ; j<=$NPeople ; j++))
do

 echo -n "Enter name of person number ($j) taking the picture: "
 read Name

 while true
  do
   echo -n "Ready? (y/n) "
   read prompt
   if [ ${prompt,,} = "y" ];
   then
    break
   fi
  done

 for (( i=1 ; i<=$NPictures ; i++))
 do
  fswebcam --no-banner "$location$Name$i.jpg" 1>/dev/null
  if [ $NPictures -gt 1 ];
  then
   echo -e "\n--You have 5 seconds to re-adjust your face for picture number ($i) --"
   sleep 5
  fi
 done

done
echo "Done!"
