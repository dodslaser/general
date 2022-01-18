#!/bin/bash -l

# This script will redo all the bindmounts for /seqstore/remote/share/gms to the sftp users located in /home/chroot
# Runs as su on seqstore

mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-southeast/gms-shared/
mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-west/gms-shared/
mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-south/gms-shared/
mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-orebro/gms-shared/
mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-uppsala/gms-shared/
mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-karolinska/gms-shared/
mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-north/gms-shared/
mount --bind /seqstore/remote/share/gms/ /home/chroot/gmc-fohm/gms-shared/
