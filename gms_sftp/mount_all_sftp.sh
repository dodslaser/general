#!/bin/bash -l

# Run as su on seqstore ONLY!!!

GMSUSERS=$(ls /home/chroot/ | grep gmc)
RESEARCHUSERS=$(ls /seqstore/remote/outbox/research_projects)

for gmsuser in $GMSUSERS ; do
    echo "binding $gmsuser"
    mount --bind /seqstore/remote/share/gms/ /home/chroot/$gmsuser/gms-shared/
done


for ruser in $RESEARCHUSERS ; do
    echo "binding $ruser"
    mount --bind /seqstore/remote/outbox/research_projects/$ruser/shared/ /home/chroot/$ruser/shared/
done


##Misc bind mounts
echo "binding archer"
mount --bind /seqstore/remote/outbox/archer/shared/ /home/chroot/archer/shared/



#mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-southeast/gms-shared/
#mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-west/gms-shared/
#mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-south/gms-shared/
#mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-orebro/gms-shared/
#mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-uppsala/gms-shared/
#mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-karolinska/gms-shared/
#mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-north/gms-shared/
#mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-fohm/gms-shared/
