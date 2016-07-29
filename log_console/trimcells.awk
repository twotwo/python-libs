BEGIN{FS="\\\\x02";OFS=","} 
{print $46, $1, $3, $4, $5, $8, $9, $10, $7, $14, $20, $28, $31, $32, $33, $34}

# u'EventID'46 ,u'logtime'1, u'AppID'3, u'UID'4, u'SDK Ver'5, u'ChannelID'8, u'Game Ver'9, u'OS'10, 
# u'IPAddr'7, u'MacAddr'14, u'DevID'20, u'AccountID'28, u'ServerID'31, u'RoleLevel'32, u'RoleID'33, u'RoleName'34,
# u'IMEI'15, u'IDFA'21, 
