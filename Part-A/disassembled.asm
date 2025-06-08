0001: b 416
0003: from-reg 0
0004: rcrd 32
0006: to-mdc
0007: from-reg 1
0008: rcrd 48
0010: to-mdc
0011: from-reg 0
0012: to-reg 2
0013: from-reg 1
0014: to-reg 3
0015: from-reg 4
0016: b-bit 0 47
0018: b-bit 1 113
0020: b-bit 2 147
0022: b-bit 3 309
0024: nop
0025: nop
0026: nop
0027: nop
0028: nop
0029: nop
0030: nop
0031: nop
0032: nop
0033: nop
0034: nop
0035: nop
0036: nop
0037: nop
0038: nop
0039: nop
0040: nop
0041: nop
0042: nop
0043: nop
0044: nop
0045: nop
0046: nop
0047: nop
0048: acc 1
0049: rarb 32
0051: clr-cf
0052: add-mba
0053: to-mba
0054: acc 0
0055: rarb 48
0057: addc-mba
0058: to-mba
0059: acc 5
0060: rarb 64
0062: to-mba
0063: from-mdc
0064: clr-cf
0065: sub-mba
0066: to-mdc
0067: r4 0
0069: bnez-cf 99
0071: nop
0072: nop
0073: nop
0074: nop
0075: nop
0076: nop
0077: nop
0078: nop
0079: nop
0080: nop
0081: ret
0082: nop
0083: nop
0084: nop
0085: nop
0086: nop
0087: nop
0088: nop
0089: nop
0090: nop
0091: nop
0092: nop
0093: nop
0094: nop
0095: nop
0096: nop
0097: nop
0098: nop
0099: nop
0100: nop
0101: rcrd 32
0103: from-mdc
0104: to-reg 0
0105: rcrd 48
0107: from-mdc
0108: to-reg 1
0109: dec*-mba
0110: nop
0111: nop
0112: nop
0113: ret
0114: nop
0115: acc 1
0116: rarb 32
0118: clr-cf
0119: add-mba
0120: to-mba
0121: acc 0
0122: rarb 48
0124: addc-mba
0125: to-mba
0126: acc 5
0127: rarb 64
0129: to-mba
0130: from-mdc
0131: clr-cf
0132: add-mba
0133: to-mdc
0134: rcrd 32
0136: from-mdc
0137: to-reg 0
0138: rcrd 48
0140: from-mdc
0141: to-reg 1
0142: addc-mba
0143: to-mba
0144: r4 0
0146: ret
0147: nop
0148: nop
0149: nop
0150: from-reg 2
0151: rarb 80
0153: to-mba
0154: from-reg 3
0155: rarb 96
0157: to-mba
0158: acc 2
0159: rarb 32
0161: clr-cf
0162: add-mba
0163: to-mba
0164: to-reg 2
0165: acc 0
0166: rarb 48
0168: addc-mba
0169: to-mba
0170: to-reg 3
0171: from-mdc
0172: rot-r
0173: to-mdc
0174: b-bit 3 203
0176: r4 0
0178: nop
0179: ret
0180: nop
0181: nop
0182: nop
0183: nop
0184: nop
0185: nop
0186: nop
0187: nop
0188: nop
0189: nop
0190: nop
0191: nop
0192: nop
0193: nop
0194: nop
0195: nop
0196: nop
0197: nop
0198: nop
0199: nop
0200: nop
0201: nop
0202: nop
0203: nop
0204: nop
0205: nop
0206: nop
0207: rarb 80
0209: from-mba
0210: rarb 32
0212: to-mba
0213: to-reg 2
0214: rarb 96
0216: from-mba
0217: rarb 48
0219: to-mba
0220: to-reg 3
0221: acc 1
0222: rarb 32
0224: clr-cf
0225: add-mba
0226: to-mba
0227: acc 0
0228: rarb 48
0230: addc-mba
0231: to-mba
0232: acc 1
0233: rarb 64
0235: to-mba
0236: from-mdc
0237: clr-cf
0238: sub-mba
0239: to-mdc
0240: r4 1
0242: bnez-cf 269
0244: ret
0245: nop
0246: nop
0247: nop
0248: nop
0249: nop
0250: nop
0251: nop
0252: nop
0253: nop
0254: nop
0255: nop
0256: nop
0257: nop
0258: nop
0259: nop
0260: nop
0261: nop
0262: nop
0263: nop
0264: nop
0265: nop
0266: nop
0267: nop
0268: nop
0269: nop
0270: nop
0271: nop
0272: nop
0273: nop
0274: rcrd 32
0276: from-mdc
0277: to-reg 0
0278: rcrd 48
0280: from-mdc
0281: to-reg 1
0282: dec*-mba
0283: nop
0284: nop
0285: nop
0286: nop
0287: nop
0288: nop
0289: nop
0290: nop
0291: nop
0292: ret
0293: nop
0294: nop
0295: nop
0296: nop
0297: nop
0298: nop
0299: nop
0300: nop
0301: nop
0302: nop
0303: nop
0304: nop
0305: nop
0306: nop
0307: nop
0308: nop
0309: nop
0310: nop
0311: nop
0312: nop
0313: nop
0314: from-reg 2
0315: rarb 80
0317: to-mba
0318: from-reg 3
0319: rarb 96
0321: to-mba
0322: acc 2
0323: rarb 32
0325: clr-cf
0326: add-mba
0327: to-mba
0328: to-reg 2
0329: acc 0
0330: rarb 48
0332: addc-mba
0333: to-mba
0334: to-reg 3
0335: from-mdc
0336: rot-l
0337: to-mdc
0338: b-bit 0 365
0340: r4 0
0342: nop
0343: nop
0344: nop
0345: nop
0346: nop
0347: nop
0348: nop
0349: nop
0350: nop
0351: nop
0352: nop
0353: nop
0354: nop
0355: nop
0356: nop
0357: ret
0358: nop
0359: nop
0360: nop
0361: nop
0362: nop
0363: nop
0364: nop
0365: nop
0366: nop
0367: nop
0368: nop
0369: nop
0370: nop
0371: rarb 80
0373: from-mba
0374: rarb 32
0376: to-mba
0377: to-reg 2
0378: rarb 96
0380: from-mba
0381: rarb 48
0383: to-mba
0384: to-reg 3
0385: acc 1
0386: rarb 32
0388: clr-cf
0389: add-mba
0390: to-mba
0391: acc 0
0392: rarb 48
0394: addc-mba
0395: to-mba
0396: acc 1
0397: rarb 64
0399: to-mba
0400: from-mdc
0401: clr-cf
0402: add-mba
0403: to-mdc
0404: rcrd 32
0406: from-mdc
0407: to-reg 0
0408: rcrd 48
0410: from-mdc
0411: to-reg 1
0412: addc-mba
0413: to-mba
0414: r4 1
0416: nop
0417: nop
0418: nop
0419: nop
0420: nop
0421: nop
0422: ret
0423: from-ioa
0424: rarb 208
0426: beqz 451
0428: from-mba
0429: b 476
0431: nop
0432: nop
0433: nop
0434: nop
0435: nop
0436: nop
0437: nop
0438: nop
0439: nop
0440: nop
0441: nop
0442: nop
0443: nop
0444: nop
0445: nop
0446: nop
0447: nop
0448: nop
0449: nop
0450: nop
0451: nop
0452: nop
0453: nop
0454: nop
0455: nop
0456: nop
0457: nop
0458: to-mba
0459: to-reg 4
0460: rarb 80
0462: nop
0463: nop
0464: call 0
0466: from-reg 4
0467: b 476
0469: nop
0470: nop
0471: nop
0472: nop
0473: nop
0474: nop
0475: nop
0476: nop
0477: nop
0478: nop
0479: nop
0480: nop
0481: nop
0482: nop
0483: nop
0484: nop
0485: nop
0486: nop
0487: nop
0488: nop
0489: nop
0490: beqz 835
0492: rarb 96
0494: acc 12
0495: xor-ba
0496: bnez 617
0498: rarb 80
0500: acc 0
0501: xor-ba
0502: b 511
0504: nop
0505: nop
0506: nop
0507: nop
0508: nop
0509: nop
0510: nop
0511: nop
0512: nop
0513: nop
0514: nop
0515: nop
0516: nop
0517: nop
0518: beqz 1311
0520: acc 5
0521: xor-ba
0522: b 531
0524: nop
0525: nop
0526: nop
0527: nop
0528: nop
0529: nop
0530: nop
0531: nop
0532: nop
0533: nop
0534: nop
0535: nop
0536: nop
0537: nop
0538: nop
0539: nop
0540: nop
0541: nop
0542: nop
0543: nop
0544: nop
0545: nop
0546: nop
0547: nop
0548: nop
0549: nop
0550: beqz 1311
0552: acc 10
0553: xor-ba
0554: b 563
0556: nop
0557: nop
0558: nop
0559: nop
0560: nop
0561: nop
0562: nop
0563: nop
0564: nop
0565: nop
0566: nop
0567: nop
0568: nop
0569: nop
0570: nop
0571: nop
0572: nop
0573: nop
0574: nop
0575: nop
0576: nop
0577: nop
0578: nop
0579: nop
0580: nop
0581: nop
0582: beqz 1311
0584: acc 15
0585: xor-ba
0586: b 595
0588: nop
0589: nop
0590: nop
0591: nop
0592: nop
0593: nop
0594: nop
0595: nop
0596: nop
0597: nop
0598: nop
0599: nop
0600: nop
0601: nop
0602: nop
0603: nop
0604: nop
0605: nop
0606: nop
0607: nop
0608: nop
0609: nop
0610: nop
0611: nop
0612: nop
0613: nop
0614: beqz 1311
0616: nop
0617: nop
0618: b 835
0620: nop
0621: nop
0622: nop
0623: nop
0624: acc 13
0625: xor-ba
0626: bnez 715
0628: rarb 80
0630: acc 4
0631: xor-ba
0632: nop
0633: nop
0634: nop
0635: nop
0636: nop
0637: nop
0638: nop
0639: nop
0640: nop
0641: nop
0642: nop
0643: nop
0644: nop
0645: nop
0646: beqz 1311
0648: acc 9
0649: xor-ba
0650: b 659
0652: nop
0653: nop
0654: nop
0655: nop
0656: nop
0657: nop
0658: nop
0659: nop
0660: nop
0661: nop
0662: nop
0663: nop
0664: nop
0665: nop
0666: nop
0667: nop
0668: nop
0669: nop
0670: nop
0671: nop
0672: nop
0673: nop
0674: nop
0675: nop
0676: nop
0677: nop
0678: beqz 1311
0680: acc 14
0681: xor-ba
0682: b 691
0684: nop
0685: nop
0686: nop
0687: nop
0688: nop
0689: nop
0690: nop
0691: nop
0692: nop
0693: nop
0694: nop
0695: nop
0696: nop
0697: nop
0698: nop
0699: nop
0700: nop
0701: nop
0702: nop
0703: nop
0704: nop
0705: nop
0706: nop
0707: nop
0708: nop
0709: nop
0710: beqz 1311
0712: nop
0713: nop
0714: b 835
0716: nop
0717: nop
0718: nop
0719: nop
0720: nop
0721: nop
0722: acc 14
0723: xor-ba
0724: b 733
0726: nop
0727: nop
0728: nop
0729: nop
0730: nop
0731: nop
0732: nop
0733: nop
0734: nop
0735: nop
0736: nop
0737: nop
0738: nop
0739: nop
0740: nop
0741: nop
0742: nop
0743: nop
0744: nop
0745: nop
0746: bnez 835
0748: rarb 80
0750: acc 3
0751: xor-ba
0752: b 761
0754: nop
0755: nop
0756: nop
0757: nop
0758: nop
0759: nop
0760: nop
0761: nop
0762: nop
0763: nop
0764: nop
0765: nop
0766: nop
0767: nop
0768: nop
0769: nop
0770: nop
0771: nop
0772: nop
0773: nop
0774: beqz 1311
0776: acc 8
0777: xor-ba
0778: b 787
0780: nop
0781: nop
0782: nop
0783: nop
0784: nop
0785: nop
0786: nop
0787: nop
0788: nop
0789: nop
0790: nop
0791: nop
0792: nop
0793: nop
0794: nop
0795: nop
0796: nop
0797: nop
0798: nop
0799: nop
0800: nop
0801: nop
0802: nop
0803: nop
0804: nop
0805: nop
0806: beqz 1311
0808: acc 13
0809: xor-ba
0810: b 819
0812: nop
0813: nop
0814: nop
0815: nop
0816: nop
0817: nop
0818: nop
0819: nop
0820: nop
0821: nop
0822: nop
0823: nop
0824: nop
0825: nop
0826: nop
0827: nop
0828: nop
0829: nop
0830: nop
0831: nop
0832: nop
0833: nop
0834: nop
0835: nop
0836: nop
0837: nop
0838: beqz 1311
0840: nop
0841: nop
0842: acc 12
0843: rarb 48
0845: to-mba
0846: rarb 96
0848: from-mba
0849: rarb 48
0851: clr-cf
0852: sub-mba
0853: b 862
0855: nop
0856: nop
0857: nop
0858: nop
0859: nop
0860: nop
0861: nop
0862: nop
0863: nop
0864: nop
0865: nop
0866: nop
0867: nop
0868: nop
0869: nop
0870: bnez-cf 1311
0872: acc 15
0873: rarb 96
0875: xor-ba
0876: bnez 901
0878: rarb 80
0880: from-mba
0881: rarb 32
0883: to-mba
0884: acc 15
0885: clr-cf
0886: sub-mba
0887: nop
0888: nop
0889: nop
0890: nop
0891: nop
0892: nop
0893: nop
0894: nop
0895: nop
0896: nop
0897: nop
0898: nop
0899: nop
0900: nop
0901: nop
0902: bnez-cf 1311
0904: nop
0905: nop
0906: nop
0907: nop
0908: acc 0
0909: rarb 64
0911: to-mba
0912: rarb 80
0914: from-mba
0915: rarb 32
0917: xor-ba
0918: rarb 64
0920: or*-mba
0921: rarb 96
0923: from-mba
0924: rarb 48
0926: xor-ba
0927: rarb 64
0929: or*-mba
0930: rarb 112
0932: from-mba
0933: rarb 64
0935: xor-ba
0936: rarb 64
0938: or*-mba
0939: from-mba
0940: beqz 1200
0942: rcrd 80
0944: from-mdc
0945: to-reg 0
0946: rcrd 96
0948: from-mdc
0949: to-reg 1
0950: rcrd 112
0952: from-mdc
0953: and-ba
0954: nop
0955: nop
0956: nop
0957: nop
0958: nop
0959: nop
0960: nop
0961: nop
0962: nop
0963: nop
0964: nop
0965: nop
0966: bnez 1311
0968: acc 0
0969: rarb 240
0971: to-mba
0972: rcrd 128
0974: from-mdc
0975: to-reg 0
0976: rcrd 144
0978: from-mdc
0979: to-reg 1
0980: rcrd 160
0982: from-mdc
0983: and*-mba
0984: rarb 208
0986: from-mba
0987: to-reg 4
0988: rarb 128
0990: nop
0991: nop
0992: nop
0993: nop
0994: nop
0995: nop
0996: nop
0997: nop
0998: nop
0999: nop
1000: nop
1001: call 0
1003: rarb 192
1005: from-mba
1006: to-reg 3
1007: rarb 48
1009: to-mba
1010: acc 1
1011: rarb 32
1013: to-mba
1014: rarb 176
1016: from-mba
1017: to-reg 2
1018: rarb 32
1020: clr-cf
1021: sub-mba
1022: to-mba
1023: from-mdc
1024: to-reg 4
1025: bnez-cf 1050
1027: nop
1028: b 1069
1030: nop
1031: nop
1032: nop
1033: nop
1034: nop
1035: nop
1036: nop
1037: nop
1038: nop
1039: nop
1040: nop
1041: nop
1042: nop
1043: nop
1044: nop
1045: nop
1046: nop
1047: nop
1048: nop
1049: nop
1050: nop
1051: nop
1052: nop
1053: nop
1054: nop
1055: nop
1056: nop
1057: rarb 48
1059: dec*-mba
1060: b 1069
1062: nop
1063: nop
1064: nop
1065: nop
1066: nop
1067: nop
1068: nop
1069: nop
1070: nop
1071: nop
1072: nop
1073: nop
1074: nop
1075: nop
1076: acc 0
1077: rarb 48
1079: xor-ba
1080: bnez 1105
1082: acc 13
1083: rarb 64
1085: to-mba
1086: rarb 32
1088: from-mba
1089: rarb 64
1091: clr-cf
1092: sub-mba
1093: bnez-cf 1246
1095: nop
1096: nop
1097: nop
1098: nop
1099: nop
1100: nop
1101: nop
1102: nop
1103: nop
1104: nop
1105: nop
1106: nop
1107: nop
1108: nop
1109: nop
1110: nop
1111: nop
1112: rarb 32
1114: from-mba
1115: to-reg 2
1116: rarb 48
1118: from-mba
1119: to-reg 3
1120: from-mdc
1121: to-reg 0
1122: from-reg 4
1123: to-mdc
1124: from-reg 0
1125: to-reg 4
1126: acc 1
1127: rarb 64
1129: to-mba
1130: rarb 32
1132: from-mba
1133: rarb 64
1135: clr-cf
1136: sub-mba
1137: to-mba
1138: bnez-cf 1163
1140: b 1069
1142: nop
1143: nop
1144: nop
1145: nop
1146: nop
1147: nop
1148: nop
1149: nop
1150: nop
1151: nop
1152: nop
1153: nop
1154: nop
1155: nop
1156: nop
1157: nop
1158: nop
1159: nop
1160: nop
1161: nop
1162: nop
1163: nop
1164: nop
1165: nop
1166: nop
1167: nop
1168: nop
1169: nop
1170: rarb 48
1172: dec*-mba
1173: nop
1174: nop
1175: nop
1176: nop
1177: nop
1178: nop
1179: nop
1180: nop
1181: nop
1182: nop
1183: nop
1184: nop
1185: nop
1186: nop
1187: nop
1188: b 1069
1190: nop
1191: nop
1192: nop
1193: nop
1194: nop
1195: nop
1196: nop
1197: nop
1198: nop
1199: nop
1200: nop
1201: nop
1202: nop
1203: nop
1204: nop
1205: nop
1206: nop
1207: acc 1
1208: rarb 240
1210: to-mba
1211: acc 1
1212: rarb 0
1214: clr-cf
1215: add-mba
1216: to-mba
1217: rarb 16
1219: addc-mba
1220: to-mba
1221: acc 1
1222: rarb 176
1224: clr-cf
1225: add-mba
1226: to-mba
1227: rarb 192
1229: addc-mba
1230: to-mba
1231: rarb 224
1233: inc*-mba
1234: b 1243
1236: nop
1237: nop
1238: nop
1239: nop
1240: nop
1241: nop
1242: nop
1243: nop
1244: nop
1245: nop
1246: nop
1247: nop
1248: nop
1249: nop
1250: nop
1251: nop
1252: nop
1253: rcrd 176
1255: from-mdc
1256: to-reg 0
1257: rcrd 192
1259: from-mdc
1260: to-reg 1
1261: rcrd 208
1263: from-mdc
1264: to-mba
1265: rcrd 80
1267: from-mdc
1268: to-reg 0
1269: rcrd 96
1271: from-mdc
1272: to-reg 1
1273: rcrd 112
1275: from-mdc
1276: and*-mba
1277: rarb 240
1279: from-mba
1280: nop
1281: nop
1282: nop
1283: nop
1284: nop
1285: nop
1286: nop
1287: beqz 416
1289: b 1314
1291: nop
1292: nop
1293: nop
1294: nop
1295: nop
1296: nop
1297: nop
1298: nop
1299: nop
1300: nop
1301: nop
1302: nop
1303: nop
1304: nop
1305: nop
1306: nop
1307: nop
1308: nop
1309: nop
1310: nop
1311: nop
1312: nop
1313: nop
1314: nop
1315: nop
1316: nop
1317: nop
1318: shutdown
1320: nop
1321: nop
1322: rarb 208
1324: from-mba
1325: rarb 160
1327: add-mba
1328: to-mba
1329: rarb 192
1331: add-mba
1332: to-mba
1333: rarb 176
1335: add-mba
1336: to-mba
1337: acc 12
1338: and*-mba