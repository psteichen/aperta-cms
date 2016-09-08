from django.db import models

# this is only used to set custom permissions:
#
#  - cms.BOARD       (member of the Management Board)
#  - cms.COMM        (communication manager)
#  - cms.MEMBER      (Member FIFTY-ONE)
#  - cms.ADMIN       (django superuser)
#
# including a little hack so that we can use these sepcific
# permissions in a choices field for HR creation
# 

class User(models.Model):
  BOARD = 'BOARD'
  COMM  = 'COMM'
  MEMBER = 'MEMBER'
  PERMISSIONS = (
      (BOARD    , 'BOARD'),
      (COMM     , 'COMM'),
      (MEMBER   , 'MEMBER'),
  )

  class Meta:
    permissions = (
      ('BOARD'  , 'Member of the Board'),
      ('COMM'   , 'Communication manager'),
      ('MEMBER' , 'Member FIFTY-ONE'),
    )


