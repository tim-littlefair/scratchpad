# Parsing 260327a-00-connect_to_fwver.json
# Message count: 119

# Frame: 822 event code:0x3e,param_length:33,le_meta_subevent:0x02,le_features:None,bd_addr:eb:2c:52:e3:5d:98,data_length:21,status:None,command_in_frame:None

# Frame: 823 event code:0x3e,param_length:12,le_meta_subevent:0x02,le_features:None,bd_addr:eb:2c:52:e3:5d:98,data_length:0,status:None,command_in_frame:None

# Frame: 824 event code:0x3e,param_length:40,le_meta_subevent:0x02,le_features:None,bd_addr:84:17:15:2b:4e:7e,data_length:28,status:None,command_in_frame:None

# Frame: 825 event code:0x3e,param_length:40,le_meta_subevent:0x02,le_features:None,bd_addr:84:17:15:2b:4e:7e,data_length:28,status:None,command_in_frame:None

# Frame: 826 event code:0x3e,param_length:40,le_meta_subevent:0x02,le_features:None,bd_addr:84:17:15:2b:4e:7e,data_length:28,status:None,command_in_frame:None

# Frame: 827 event code:0x3e,param_length:32,le_meta_subevent:0x02,le_features:None,bd_addr:84:17:15:2b:4e:7e,data_length:20,status:None,command_in_frame:None

# Frame: 828 command 03f:0157 3: 
hcitool lealclr
hcitool lealadd 84:17:15:2b:4e:7e
sleep 2
sleep 2
hcitool cmd 0x3f 0x0157 0x00 0x00 0x00

# Frame: 829 event code:0x0e,param_length:7,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:828

# Frame: 830 command 03f:0157 3: 

# Frame: 831 event code:0x0e,param_length:7,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:830

# Frame: 832 command 03f:0157 3: 

# Frame: 833 event code:0x0e,param_length:7,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:832

# Frame: 834 command 008:000c 2: None

# Frame: 835 event code:0x0e,param_length:4,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:0x00,command_in_frame:834

# Frame: 836 command 008:000b 7: None
# "bthci_cmd.param_length": "7",
# "bthci_cmd.le_scan_type": "0x01",
# "bthci_cmd.le_scan_interval": "8000",
# "bthci_cmd.le_scan_window": "3200",
# "bthci_cmd.le_own_address_type": "0x01",
# "bthci_cmd.le_scan_filter_policy": "0x00"
hcitool cmd 0x08 0x000b 0x01 0x80 0x00 0x32 0x00 0x01 0x00



# Frame: 837 event code:0x0e,param_length:4,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:0x00,command_in_frame:836

# Frame: 838 command 008:000b 7: None

# Frame: 839 event code:0x0e,param_length:4,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:0x00,command_in_frame:838

# Frame: 840 command 008:000c 2: None
# "bthci_cmd.param_length": "2",
# "bthci_cmd.le_scan_enable": "0x01",
# "bthci_cmd.le_filter_duplicates": "0x00"
hcitool cmd 0x08 0x000c 0x01 0x00


# Frame: 841 event code:0x0e,param_length:4,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:0x00,command_in_frame:840

# Frame: 842 event code:0x3e,param_length:33,le_meta_subevent:0x02,le_features:None,bd_addr:eb:2c:52:e3:5d:98,data_length:21,status:None,command_in_frame:None

# Frame: 843 event code:0x3e,param_length:12,le_meta_subevent:0x02,le_features:None,bd_addr:eb:2c:52:e3:5d:98,data_length:0,status:None,command_in_frame:None

# Frame: 844 command 008:000d 25: None
hcitool lecc 84:17:15:2b:4e:7e

# Frame: 845 event code:0x0f,param_length:4,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:0x00,command_in_frame:844

# Frame: 846 event code:0x3e,param_length:33,le_meta_subevent:0x02,le_features:None,bd_addr:e9:ca:24:e4:4e:8b,data_length:21,status:None,command_in_frame:None

# Frame: 847 event code:0x3e,param_length:31,le_meta_subevent:0x0a,le_features:None,bd_addr:84:17:15:2b:4e:7e,data_length:None,status:0x00,command_in_frame:844

# Frame: 848 command 008:0016 2: None
hcitool leinfo 84:17:15:2b:4e:7e

# Frame: 849 event code:0x0f,param_length:4,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:0x00,command_in_frame:848

# Frame: 850 event code:0x3e,param_length:11,le_meta_subevent:0x07,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 851 attribute 0x02 None None
# Frame: 851 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:7,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 852 attribute 0x03 None None
# Frame: 852 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:7,data:,mode:-1,src.name:Nexus 5X

# Frame: 853 command 008:0013 14: None

# Frame: 854 attribute 0x10 None None
# Frame: 854 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 855 event code:0x0f,param_length:4,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:0x00,command_in_frame:853

# Frame: 856 event code:0x3e,param_length:12,le_meta_subevent:0x04,le_features:0x000000000000413f,bd_addr:None,data_length:None,status:0x00,command_in_frame:848

# Frame: 857 command 001:001d 2: None

# Frame: 858 event code:0x0f,param_length:4,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:0x00,command_in_frame:857

# Frame: 859 event code:0x3e,param_length:10,le_meta_subevent:0x03,le_features:None,bd_addr:None,data_length:None,status:0x3b,command_in_frame:853

# Frame: 860 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 861 event code:0x3e,param_length:11,le_meta_subevent:0x07,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 862 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 863 attribute 0x11 None None
# Frame: 863 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:18,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 864 attribute 0x10 None None
# Frame: 864 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 865 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 866 event code:0x0c,param_length:8,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:0x00,command_in_frame:857

# Frame: 867 event code:0x3e,param_length:11,le_meta_subevent:0x07,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 868 attribute 0x11 None None
# Frame: 868 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:46,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 869 attribute 0x08 None None
# Frame: 869 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 870 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 871 attribute 0x01 0x0001 None
# Frame: 871 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:9,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 872 attribute 0x08 None None
# Frame: 872 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 873 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 874 attribute 0x09 None None
# Frame: 874 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:20,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 875 attribute 0x08 None None
# Frame: 875 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 876 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 877 attribute 0x01 0x0006 None
# Frame: 877 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:9,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 878 attribute 0x04 None None
# Frame: 878 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:9,data:,mode:-1,src.name:Nexus 5X

# Frame: 879 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 880 attribute 0x05 None None
# Frame: 880 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:10,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 881 attribute 0x08 None None
# Frame: 881 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 882 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 883 attribute 0x01 0x0007 None
# Frame: 883 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:9,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 884 attribute 0x08 None None
# Frame: 884 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 885 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 886 attribute 0x09 None None
# Frame: 886 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:20,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 887 attribute 0x08 None None
# Frame: 887 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 888 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 889 attribute 0x01 0x000b None
# Frame: 889 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:9,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 890 attribute 0x08 None None
# Frame: 890 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 891 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 892 attribute 0x01 0x000c None
# Frame: 892 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:9,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 893 attribute 0x08 None None
# Frame: 893 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 894 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 895 attribute 0x09 None None
# Frame: 895 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:69,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 896 attribute 0x08 None None
# Frame: 896 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 897 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 898 attribute 0x01 0x0013 None
# Frame: 898 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:9,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 899 attribute 0x04 None None
# Frame: 899 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:9,data:,mode:-1,src.name:Nexus 5X

# Frame: 900 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 901 attribute 0x05 None None
# Frame: 901 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:10,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 902 attribute 0x04 None None
# Frame: 902 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:9,data:,mode:-1,src.name:Nexus 5X

# Frame: 903 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 904 attribute 0x05 None None
# Frame: 904 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:10,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 905 attribute 0x08 None None
# Frame: 905 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 906 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 907 attribute 0x01 0x0015 None
# Frame: 907 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:9,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 908 attribute 0x08 None None
# Frame: 908 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 909 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 910 attribute 0x09 None None
# Frame: 910 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:48,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 911 attribute 0x08 None None
# Frame: 911 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:11,data:,mode:-1,src.name:Nexus 5X

# Frame: 912 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 913 attribute 0x01 0x001b None
# Frame: 913 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:9,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 914 attribute 0x04 None None
# Frame: 914 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:9,data:,mode:-1,src.name:Nexus 5X

# Frame: 915 event code:0x3e,param_length:33,le_meta_subevent:0x02,le_features:None,bd_addr:e9:ca:24:e4:4e:8b,data_length:21,status:None,command_in_frame:None

# Frame: 916 event code:0x3e,param_length:12,le_meta_subevent:0x02,le_features:None,bd_addr:e9:ca:24:e4:4e:8b,data_length:0,status:None,command_in_frame:None

# Frame: 917 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 918 attribute 0x05 None None
# Frame: 918 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:14,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 919 attribute 0x04 None None
# Frame: 919 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:9,data:,mode:-1,src.name:Nexus 5X

# Frame: 920 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 921 attribute 0x05 None None
# Frame: 921 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:14,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 922 attribute 0x04 None None
# Frame: 922 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:9,data:,mode:-1,src.name:Nexus 5X

# Frame: 923 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 924 attribute 0x01 0x001e None
# Frame: 924 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:9,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 925 command 008:0013 14: None

# Frame: 926 event code:0x0f,param_length:4,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:0x00,command_in_frame:925

# Frame: 927 attribute 0x12 0x0018 None
# Frame: 927 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:9,data:,mode:-1,src.name:Nexus 5X

# Frame: 928 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 929 event code:0x3e,param_length:10,le_meta_subevent:0x03,le_features:None,bd_addr:None,data_length:None,status:0x3b,command_in_frame:925

# Frame: 930 attribute 0x13 0x0018 None
# Frame: 930 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:5,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 931 attribute 0x52 0x001b 35:00:02:1a:00
# Frame: 931 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:12,data:,mode:-1,src.name:Nexus 5X

# Frame: 932 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 933 attribute 0x52 0x001b 35:00:05:0a:03:c2:01:00
# Frame: 933 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:15,data:,mode:-1,src.name:Nexus 5X

# Frame: 934 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 935 attribute 0x52 0x001b 35:00:04:0a:02:3a:00
# Frame: 935 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:14,data:,mode:-1,src.name:Nexus 5X

# Frame: 936 attribute 0x52 0x001b 35:00:04:0a:02:72:00
# Frame: 936 acl: chandle:0x0002,pb_flag:0,bc_flag:0,length:14,data:,mode:-1,src.name:Nexus 5X

# Frame: 937 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 938 event code:0x13,param_length:5,le_meta_subevent:None,le_features:None,bd_addr:None,data_length:None,status:None,command_in_frame:None

# Frame: 939 attribute 0x1b 0x0017 35:00:0e:12:0c:08:02:32:08:0a:06:31:2e:30:2e:32:39
# Frame: 939 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:24,data:,mode:-1,src.name:Mustang Micro Plus

# Frame: 940 acl: chandle:0x0002,pb_flag:2,bc_flag:0,length:123,data:,mode:-1,src.name:Mustang Micro Plus
