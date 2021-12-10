import re
import openpyxl
import time
from datetime import timedelta

start_time = time.time()

from openpyxl import Workbook, load_workbook
#Input below the name of the spreadsheet including extension. It needs to be .xlsx
wb = load_workbook("Clean_3_Login_intents_with_latest_script.xlsx")
#Input below the name of the Sheet (e.g. "Sheet1")
source = wb["Sheet1"]

text = []

#Input below the name of the column with the raw data that you want cleaned
for cell in source['A']:
    # print(type(str(cell.value)))
    text.append(cell.value.lower())

clean_text = []

replacements = [
    ('hi team', ''),
    # ('>.+$', ''),
    # ('^\s?>.*(\w*\W*)*', ''),
    # ('^\s?>(\W*\w*)*', ''), #Didn't work although it did on regex101
    ('hi there', ''),
    ('hi everyone', ''),
    ('hello team', ''),
    ('hello there', ''),
    ('hello everyone', ''),
    ('how are you', ''),
    ('\\bhi\\b', ' '),
    ('this\se-?mail along with(\W+\w+)+pient', ''), #Interestingly this longer pattern worked - note that it's lacking angle brackets
    ('original message', ''),
    ('original email', ''),
    ('guaranteed\s*virus-free\.?\s?www\.avast\.com', ''),
    ('the absence(\W+\w+)+ivirus', ''),
    # ('free of viruses;?', ''),
    ('free\W(from|of) viruses', ''),
    ('this (e-?mail|message) has been checked for viruses( (with|by) avast antivirus( software)?)?', ''),
    ('by avast antivirus-software\.\s?https://www\.avast\.com/antivirus', ''),
    ('by avast antivirus-software', ''),
    ('if this payment has not been authorized by you\.?\s*contact the team immediately', ''),
    ('if you have not made this change, let us know immediately', ''),
    ('configuration_email_images_paysafecard-logo\.gif', ''),
    # ('there have been several failed(\W+\w+)*uigley', ''),#
    ('if you have any questions', ''),
    ('our service team will be happy to assist you', ''),
    ('this is an automatically generated email', ''),
    ('you can\'t respond directly to it', ''),
    ('you can\'t reply directly', ''),
    ('www\.paysafecard\.com', ''),
    ('copyright.+international', ''),
    # ('virus-free\. www\.avg\.com', ''),
    ('virus-free', ''),
    ('www\.avast\.com(antivirus)?', ''),
    ('www\.avg\.com', ''),
    ('\\bhellos?\\b', ' '),
    ('ã©', 'e'), #encoding issues
    ('ã³', 'o'), #encoding issues
    ('ã¶', 'o'), #encoding issues
    ('\\bsalve\\b', ''),
    ('query the threatmetrix api', ''),
    ('have a (nice|good) weekend', ''),
    ('i hope you had a pleasant weekend', ''),
    ('technical operations specialist, paysafecard', ''),
    # ('copyright.+\W+.+gley', ''),
    ('copyright(\W+\w+)+gley', ''),
    ('paysafe prepaid services limited(\W+\w+)+gley', ''),
    # ('paysafe prepaid services limited', ''),
    # ('paysafe prepaid services limited, grand canal house, grand canal street', ''),#
    # ('upper, dublin 0, d00 y0r0, ireland', ''),#
    ('company registration number', ''),
    ('grand(\W+\w+)+land', ''),
    ('(irish )?company number', ''),
    # ('copyright â© paysafecard.com wertkarten gmbh\. all rights reserved', ''),#
    # ('paysafecardâ® is a registered trademark of paysafecard.com wertkarten gmbh', ''),#
    # ('paysafe prepaid services limited, under the trade name paysafecard', ''),#
    # ('my paysafecard, paysafecard mastercard and paysafecash, is regulated by the', ''),#
    # ('the central bank of ireland\. directors: e\. allen, m\. currid, h\. gerhartinger', ''),#
    # ('\(at\), k\. maragkakis \(gr\), j\. mcgee, p\. miley, u\. mã¼ller \(at\), d\. quigley', ''),#
    # ('paysafe prepaid.+quigley', ''),#
    ('an error occurred  the paysafecard payment site could not be connected\. we thank you for your understanding\.the paysafecard team', ''),
    ('this e-mail and all attached files are confidential and are intended to  only  addressees appointed above\. if you have received this e-mail  by mistake, or  you are not the addressee mentioned above, please inform  sender and delete  this e-mail, including any attached files  copies\. if  you are not an authorized addressee of this e-mail, you are not  authorised information in  contained in any way, publish, disseminate or  otherwise taken', ''),
    ('think before you print', ''),
    ('paysafe prepaid services limited(, trading as paysafecard, my paysafecard,\Wpaysafecard mastercard and paysafecash, is regulated by the central bank of\Wireland)?', ''),
    # ('paysafe prepaid services limited, trading as paysafecard, my paysafecard', ''),#
    # ('paysafecard mastercard and paysafecash, is regulated by the central bank of', ''),#
    # ('^ireland\\b', ''),#
    ('refer to https://www.paysafe\.com/legal-and-compliance/regulatory-disclosure/ for corporate and regulatory disclosures regarding members of the paysafe group\.\s*the paysafe group archives and monitors outgoing and incoming e-mail\.\s*the contents of this email, including any attachments, are confidential to the ordinary user of the email address to which it was addressed\.\s*if you are not the addressee of this email you may not copy, forward, disclose or otherwise use it or any part of it in any form whatsoever\.\s*the paysafe group accepts no liability for any errors or omissions arising as a result of transmission\.?', ''),
    ('email\.\s?address@domain\.\s?com', ''),
    ('\w+@\w+\.\w+(\.\w+)?', ''),
    ('new email:\s*', ''),
    ('\[no object]', ''),
    ('\[not scanned]', ''),
    ('\(scan0get\)', ''),
    # ('subject: \[external]', ''),#
    ('\[external]', ''),
    ('retroalimentacion - paysafecard', ''),
    # ('retroalimentacion', ''),#
    # ('feedback - paysafecard 0\.0\.0', ''),#
    # ('opinion - paysafecard 0\.0\.0', ''),#
    # ('feedback - paysafecard 0\.0+', ''),#
    ('feedback - paysafecard', ''),
    ('feedback-paysafecard', ''),
    ('opinion - paysafecard', ''),
    ('others others', ''),
    ('get outlook for androidhttps://aka\.ms/ghei00', ''),
    ('get outlook<https://aka\.ms/qtex0l> for', ''),
    ('paysafe prepaid services limited, grand canal house, grand channel street upper, dublin 0, d00 y0r0, ireland   company registration number: 000000  copyright \? paysafecard\.com wertkarten gmbh\. all rights reserved\. paysafecard\? is a registered trademark of paysafecard\.com wertkarten gmbh\. paysafe prepaid services limited, with the trade name paysafecard, my paysafecard, paysafecard mastercard and paysafecash, is regulated by the central bank of ireland\. directors: e\. allen, m\. currid, h\. gerhartinger (at), k\. maragkakis (gr), j\. mcgee, p\. miley, u\. muller (at), d\. quigley', ''),
    ('freemail powered by mail\.de - more security, seriousness and comfort', ''),
    ('this message was sent from my android mobile phone with web\.?de mail', ''),
    ('this message was sent from my android mobile phone with web de mail', ''),
    ('this message was sent from my android mobile phone with 0&0 mail', ''),
    ('sent from my android phone with 0&0 mail', ''),
    ('sent by virgilio email', ''),
    ('sends from my egg phone', ''),
    ('vanuit mail<https:gomicrosoftcomfwlinklinkid=> voor windows', ''),
    ('(verzonden )?vanuit mail.+voor windows', ''),
    ('envoys set yahoo mail for android', ''),
    ('verstuurd vanaf mijn iphone', ''),
    ('trimis din yahoo mail pe android', ''),
    ('trimis din mail pentru windows', ''),
    ('trimis de pe iphone-ul meu', ''),
    ('trimis de pe( telefonul meu huawei)?', ''),
    ('outlook voor android<https:akamsaabysg> downloaden', ''),
    ('outlook voor android<https://aka\.ms/aab0ysg> downloaden', ''),
    ('outlook voor android downloaden', ''),
    ('sent from the orange mail application', ''),
    ('sent from my orange phone', ''),
    ('download typeapp for android', ''),
    # ('sent by mailhttps://go\.microsoft\.com/fwlink/\?linkid=000000 for windows 00', ''),#
    # ('sent from the <https://go\.microsoft\.com/fwlink/\?linkid=000000> to windows', ''),#
    ('sent by e?mail<https://go\.microsoft\.com/fwlink/\?linkid=000000> for windows', ''),#
    # ('sent from e?mailhttps://go\.microsoft\.com/fwlink/\?linkid-000000 for windows', ''),#
    ('sent from e?mail<https://go\.microsoft\.com/fwlink/\?linkid=000000> for windows', ''),
    # ('sent by e?mail https://go\.microsoft\.com/fwlink/\?linkid=000000> for windows', ''),#
    # ('sent from e?mail <\s?https://go\.microsoft\.com/fwlink/; linkid = 000000 "for windows', ''),#
    ('origin: mail<https:gomicrosoftcomfwlinklinkid=> for windows', ''),
    # ('sent from e?mail<https:gomicrosoftcomfwlinklinkid=> for windows', ''),#
    # ('sent by e?mail<https:gomicrosoftcomfwlinklinkid=> for windows', ''),#
    # ('sent from the <https:gomicrosoftcomfwlinklinkid=> to windows', ''),#
    # ('sent from e?mail app<https:gomicrosoftcomfwlinklinkid=> for windows', ''),#
    # ('sent from e?mail app<https://go\.microsoft\.com/fwlink/\?linkid=000000> for windows', ''),#
    # ('sent from windows <https:gomicrosoftcomfwlinklinkid=>', ''),#
    # ('sent from mail apphttps://go\.microsoft\.com/fwlink/\?linkid=000000 for windows 00', ''),#
    # ('sent from mailhttps://go\.microsoft\.com/fwlink/\?linkid=000000 for windows 00', ''),#
    ('sent from mobile huawei', ''),
    ('sent from my galaxy device', ''),#
    ('was sent from my galaxy', ''),
    ('sent from my galaxy', ''),
    ('from my galaxy device', ''),
    ('von meinem iphone gesendet', ''),
    ('gesendet von mail fur windows', ''),
    # ('sent from my huawei mobile device', ''),#
    ('sent from my huawei mobile phone', ''),
    ('sent from my huawei mobile', ''),
    ('transmitted from my huawei phone', ''),
    ('sent from my huawei phone', ''),
    ('sent from my huawei tablet', ''),
    ('sent from my ipad', ''),
    # ('sent from my iphone', ''),#
    ('sent from my mobile huawei', ''),
    ('sent from my phone huawei', ''),
    # ('sent from my samsung device', ''),#
    ('sent from my samsung galaxy smartphone', ''),#
    # ('sent from the samsung gala smartphone', ''),#
    ('sent from my smartphone in play', ''),
    ('sent from my smartphone samsung galaxy', ''),
    ('sent from the new aol app for android', ''),
    ('sent from the all-new aol app for ios', ''),
    ('sent from the new aol-app for android', ''),
    ('sent from the new aol-app for ios', ''),
    ('sent from my tablet huawei', ''),
    # ('sent from my t-mobile 0g lte device', ''),#
    ('sent from outlookhttp://aka\.ms/weboutlook', ''),
    ('sent from samsung galaxy-a00 powered by three', ''),
    ('sent from samsung galaxy-a00 powered by', ''),
    ('sent from samsung galaxy-a00', ''),
    # ('sent from samsung device', ''),#
    ('(was )?sent from samsung galaxy smartphone', ''),#
    ('sent from samsung galaxy', ''),
    ('sent from samsung tablet', ''),
    ('sent from samsung mobile', ''),
    # ('sent from samsung phone', ''),#
    ('sent from the https://go\.microsoft\.com/fwlink/\?linkid=000000 to windows', ''),
    ('sent from the mail apphttps://go\.microsoft\.com/fwlink/\?linkid=000000 for windows', ''),
    ('sent from the mail app<https://go\.microsoft\.com/fwlink/\?linkid=000000> for windows', ''),
    ('sent from the mobile app itunes\.apple\.com wp mail', ''),
    ('sent from the samsung galaxy smartphone', ''),#
    # ('sent from yahoo mail for iphone', ''),#
    ('sent from yahoo mail on andmroid', ''),
    ('sent from yahoo mail on android', ''),
    ('sent from yahoo mail to android', ''),
    # ('sent from yahoo mail to iphone', ''),#
    ('sent from yahoo mail with android', ''),
    ('sent from yahoo mail to android', ''),
    ('sent by yahoo mail to android', ''),
    ('sent from yahoo mail\. get the app', ''),
    ('sent by yahoo mail\. download the app', ''),
    ('sent from yahoo mail on android', ''),
    ('sent from yahoo mail for android\\b', ''),
    # ('sent by yahoo mail for iphone', ''),#
    # ('sent from outlook email app for android', ''),
    ('sent from outlook (app )?email app for android', ''),
    ('sent via the outlook email app app for android', ''),
    ('sent by yahoo mail on android', ''),
    ('sent via yahoo mail on android', ''),
    ('sent via gmail mobile', ''),
    ('sent from gmail mobile', ''),
    ('sent from gmail to mobile', ''),
    ('sent with gmail mobile', ''),
    ('sent by gmail mobile', ''),
    ('sent from my telcel samsung mobile', ''),
    ('sent via yahoo email app for android', ''),
    ('yahoo mail on android', ''),
    ('sent by yahoo post office on android', ''),
    ('sent with the telekom mail app', ''),
    ('sent with the gmx mail app', ''),
    ('sent with the gmx iphone app', ''),
    ('sent sent by my/my galaxy', ''),
    ('sent by my/my galaxy', ''),
    ('sent from my\s?/\s?my galaxy', ''),
    ('sent with my/my galaxy', ''),
    ('sent via my/my galaxy', ''),
    ('<https:kommunikationsdienstetonlinederedirectsemail_app_android_sendmail_footer>', ''),
    ('sent by my samsung galaxy smartphone', ''),#
    ('sent by samsung galaxy smartphone', ''),#
    ('sent off galaxy', ''),
    ('sent on galaxy', ''),
    ('sent to windows 00 post  -- this email has been scanned by avast antivirus software\. https://www\.avast\.com/antivirus', ''),
    ('sent with my redmi 0x', ''),
    ('sent (with|using) the mobile mail app', ''),
    ('sent with the web\.?de ipad app', ''),
    ('sent with the web\.?de iphone app', ''),
    ('sent with the web\.?de app', ''),
    ('sent with the web\.?de mail app', ''),
    ('sent from the mobile app wp mail', ''),
    ('sent from my mi mix', ''),
    ('sent by windows 00 post', ''),
    ('sent by windows mail', ''),
    ('sent from windows mail', ''),
    ('sent by windows', ''),
    ('sent from windows', ''),
    ('sent from onetmail', ''),
    ('sent from protonmail (mobile|for ios)?', ''),
    ('sent from my redmi', ''),
    ('sent from my android phone with web\.?de mail', ''),
    ('sent from my android phone with mail\.com mail', ''),
    ('sent from my android phone with mail\.com', ''),
    ('horizon management photography & model agency portrait design body design image design lutzelstr de two bridges email instagram hm_pm_agency', ''),
    ('the paysafecard team will ensure that your case is handled as soon as possible with a 00000000 reference number', ''),
    ('this email originated from outside of paysafe\. do not click links or open attachments unless you trust the sender and know the content is safe', ''),
    ('visitor message from alivechat @ 0/0/0000 0:00:00 pm', ''),
    ('visitor message from alivechat @ 0/00/0000 0:00:00 pm', ''),
    ('(blank)', ''),
    ('forwarded message -+ by:', ''),
    ('forwarded message -+ de:', ''),
    ('forwarded message', ''),
    ('date: fri, 00 mar 0000, 00:00 subject:', ''),
    ('this message was sent from my android mobile phone with gmx mail', ''),
    ('this message was sent from my android mobile phone with & mail', ''),
    ('dese message was sent from my android mobile phone with gmx mail', ''),
    ('sent from my android phone with gmx mail', ''),
    ('excuse my brevity', ''),
    ('sent with the telekom mail app https://kommunikationsdienste\.t-online\.de/redirects/email_app_android_sendmail_footer', ''),
    ('sent with the telekom mail app <https:kommunikationsdienstetonlinederedirectsemail_app_android_sendmail_footer>', ''),
    ('this e-mail has been scanned for viruses by avast antivirus-software\. https://www\.avast\.com/antivirus', ''),
    ('sent from mymail for ios', ''),
    ('sent by (my|libero )mail (for|per) ios', ''),
    ('sent via mymail for ios', ''),
    ('sent from mymail( app)? for android', ''),
    ('sent by mymail for android', ''),
    ('sent via mymail for android', ''),
    ('our service team is happy to help you', ''),
    ('with friendly grussen', ''),
    ('\\bgruss\\b', ''),
    ('\\bgroetjes\\b', ''),
    # ('to whom it may concern', ''),
    ('dear all', ''),
    ('dear colleagues', ''),
    ('mit freundlichen gru.*en', ''),
    ('your feedback is valued! help us improve your experience by rating us below', ''),
    ('dear customer service from paysafecard', ''),
    ('dear dams and lords', ''),
    ('dear ladies and gentlemen', ''),
    ('dear lady', ''),
    ('dear lord ma\'am', ''),
    ('dear me', ''),
    ('dear paysafe card team', ''),
    ('dear paysafe employe+s?', ''),
    ('dear paysafe team', ''),
    ('dear paysafec[ao]rd team', ''),
    ('dear paysafecard', ''),
    ('dear paysafeteam', ''),
    ('dear paysafe\\b', ' '),
    ('dear reader', ''),
    ('dear service team', ''),
    ('dear sir, ma\'ame?', ''),
    ('dear sir, madame?', ''),
    ('dear sir/madame?', ''),
    ('dear sir/madame?:', ''),
    ('dear sir madam', ''),
    ('dear sir or madame?', ''),
    ('dear sirs?', ''),
    ('dear sup+ort from paysafecard', ''),
    ('dear sup+ort team', ''),
    (' dear paysafecard team', ''),
    ('dear team of paysafecard', ''),
    ('dear team', ''),
    ('dear mr/mrs', ''),
    ('dear customer', ''),
    ('dear', ''),
    ('mr/mrs', ''),
    ('sir/ma[d\']ame?', ''),
    ('sirs?/madame?s', ''),
    ('\\bsir\\b', ''),
    ('\\bmadame?\\b', ''),
    ('customer service paysafecard', ''),
    ('customer service paysafe card', ''),
    ('smartphone samsung galaxy', ''),
    ('samsung galaxy smartphone', ''),
    ('external email: beware o[fr] phishing attacks!', ''),
    ('external email: beware o[fr] phishing tackles!', ''),
    ('get outlook for android < https://aka\.ms/ghei00 "', ''),
    ('get outlook for ioshttps://aka\.ms/o0ukef', ''),
    ('get outlook for ioshttps://aka\.ms/o0ukef app', ''),
    ('outlook for ios<https://aka\.ms/o0ukef> download', ''),
    ('outlook for ios.+download', ''),
    ('"outlook" \(android\) https://aka\.ms/ghei00>', ''),
    ('obtener outlook para android', ''),
    ('obtener outlook para ios', ''),
    ('telecharger outlook pour android', ''),
    ('get the outlook for ios', ''),
    ('get outlook for ios', ''),
    ('get outlook (para|pentru) android', ''),
    ('enviado desde mi (telefono|iphone)', ''),
    ('inviato dal mio telefono', ''),
    ('inviato da yahoo mail su android', ''),
    ('enviado from my galaxy', ''),
    ('envoye de mon iphone', ''),
    ('enviado do meu iphone', ''),
    ('enviado do meu', ''),
    ('good afternoon', ''),
    ('good\s?bye', ''),
    ('have a good day', ''),
    ('wish you a', ''),
    ('good day', ''),
    ('good evening', ''),
    ('good morning', ''),
    ('a happy new year', ''),
    ('happy new year', ''),
    ('a merry christmas', ''),
    ('merry christmas', ''),
    ('have a good night', ''),
    ('good\s?night', ''),
    ('good tag', ''),
    ('good vece+r', ''),
    ('good ziua', ''),
    ('buna ziua', ''),
    ('good sea?ra', ''),
    ('good to you', ''),
    ('\\bm[au]m\\b', ' '),
    ('\[image/png]', ''),
    ('\[image]', ''),
    ('\[image.+]', ''),
    ('\[picture]', ''),
    ('\(mailto:\)', ''),
    ('<mailto:>', ''),
    ('no subject', ''),
    ('bua evening', ''),
    ('with kind greetings?', ''),
    ('greet with kind', ''),
    ('with friendly greetings?', ''),
    ('with best greetings?', ''),
    ('with sincere greetings?', ''),
    ('sincere greetings?', ''),
    ('kind greetings?', ''),
    ('friendly greetings?', ''),
    ('best greetings?', ''),
    ('many greetings?', ''),
    ('a greetings?', ''),
    ('greetings?', ''),
    ('\\bgreets?\\b', ''),
    ('\\bbest,', ''),
    # ('with kind regards?', ''),#
    # ('with best regards?', ''),#
    # ('with friendly regards?', ''),#
    ('with (good|best|kind|friendly) regards?', ''),
    ('friendly regards?', ''),
    ('kind regards?', ''),
    ('best regards?', ''),
    ('with regards?', ''),
    ('regards?', ''),
    ('best wishes', ''),
    ('with friendly', ''),
    ('have a nice day', ''),
    ('guys', ''),
    ('\\bhal*o\\b', ' '),
    ('get outlook for android<https:akamsghei>', ''),
    ('get outlook for android<https:akamsaabysg>', ''),
    ('download outlook for android', ''),
    ('outlook for android<https:akamsaabysg> download', ''),
    ('download outlook for android<https://aka\.ms/aab0ysg>', ''),
    ('download outlook for ios', ''),
    ('outlook for android<https://aka\.ms/aab0ysg> download', ''),
    ('outlook for ios<https:akamsoukef> download', ''),
    ('sent by app from mail\.ru for ios?', ''),
    ('sent by my galaxy', ''),
    ('sent by my mobile huawei', ''),
    ('sent by protonmail mobile', ''),
    ('sent with \[protonmail]', ''),
    ('sent with protonmail secure email', ''),
    # ('sent by sony xperia\? smartphone', ''),#
    # ('sent by sony xperia smartphone', ''),#
    # ('sent from sony xperia smartphone', ''),#
    ('sent from sony xperia', ''),
    # ('sent from a mobile phone\. huawei devices', ''),#
    # ('sent from android device', ''),#
    ('sent by free e?mail for ios', ''),
    ('sent by free e?mail for android', ''),
    ('sent from free e?mail to android', ''),
    ('sent with the 0&0 mail app', ''),
    ('get\s?outlook for android', ''),
    ('sent via outlook email app for android', ''),
    ('outlook for android', ''),
    ('sent from galaxy', ''),
    # ('sent from huawei mobile phone', ''),#
    ('sent from huawei mobile', ''),
    # ('sent from huawei phone', ''),#
    ('sent from mobile', ''),
    # ('sent from the iphone', ''),#
    # ('sent from iphone', ''),#
    # ('sent with my iphone', ''),#
    # ('sent from mail app for windows', ''),#
    ('shipped from iphone', ''),
    ('shipped from my galaxy', ''),
    ('sent from the galaxy', ''),
    ('from my/my galaxy sent', ''),
    # ('sent by mail for windows', ''),#
    ('sent from outlook', ''),
    ('sent by ipad', ''),
    ('sent from ipad', ''),
    ('sent via ipad', ''),
    ('sent with ipad', ''),
    ('sent from the mobile email app', ''),
    ('<https:akamsaabysg>', ''),
    # ('huawei', ''),
    # ('samsung', ''),
    # ('galaxy', ''),
    # ('iphone', ''),
    # ('ipad', ''),
    ('see you soon', ''),
    ('ï.+ï…', ''),
    ('î.+android', ''),
    # ('android', ''),
    # ('hello paysafe card team', ''),
    # ('hello paysafe company', ''),
    # ('hello paysafe team', ''),
    # ('hello paysafecard', ''),
    ('yours sincerely', ''),
    ('yours truly', ''),
    ('\\byours\\b', ' '),
    ('(very\s)?sincerely', ''),
    ('(very\s)?faithfully', ''),
    ('(very\s)?kindly', ''),
    ('with kindness', ''),
    ('(very\s)?cordial+y', ''),
    ('cordialement', ''),
    ('(very\s)?nicely', ''),
    ('(very\s)?warmly', ''),
    ('(very\s)?politely', ''),
    ('respectfully', ''),
    ('regardsialy', ''),
    ('our service.*:', ''),
    ('the paysafecard team', ''),
    ('your paysafecard team', ''),
    ('paysafecard team', ''),
    ('team of paysafecard', ''),
    ('please', ''),
    ('name name', ''),
    ('mr name', ''),
    ('\\bpls\\b', ''),
    ('\\bm[fv]g\\b', ' '),
    ('\\b[fv]g\\b', ' '),
    ('\\bl[gp]\\b', ' '),
    ('\\bl\.g\\b', ' '),
    ('\\bhey\\b', ' '),
    # ('c?allguid:', ''),#
    # ('017c83d4-ef73-4a3a-acae-6113047f86d0', ''),#
    # ('017ca78c-0ab2-4426-bb09-cec862a6c743', ''),#
    # ('017ca7b5-71da-4428-81b9-308c7b896faf', ''),#
    # ('017c92d8-a184-4f53-b7a4-b03d327c2bdb', ''),#
    # ('017c272c-9dd7-4d4c-8963-babe35554d6b', ''),#
    # ('017c554e-9aa7-40f5-ba55-c04e17190d98', ''),#
    # ('017[cb].+\\b', ''),
    ('[kc][ow]di[kc]os?', 'code'), #Greek
    ('[kc][ow]di[kc]oi', 'codes'), #Greek
    ('psiphi[oa]', 'digit'), #Greek
    ('psifi[oa]', 'digit'), #Greek
    ('insurance code', 'security code'),
    ('\\bloghi?ez\\b', 'login'), #Romanian
    ('\\bucet\\b', 'account'), #Slovak
    ('\\bcontu\\b', 'account'), #Romanian
    ('h[ae]slo', 'password'), #Czech
    ('passwort', 'password'), #German
    # ('\\bblokat\\b', 'blocked'), #Romanian - check
    # ('cmr verified', ''),
    ('<#dab0fad0-0dd0-00bb-a0b0-0e0aa0f0fdf0>', ''),
    ('\d+/+', ' '),
    # ('\d{2,}/+', ' '),
    ('\d+', ' '),
    # ('\d{2,}', ' '),
    ('\\bdear\\b', ' '),
    ('visitor message from alivechat @ // :: [ap]m', ''),
    ('visitor message from alivechat @', ''),
    ('sent from the mail\.ru app for android', ''),
    ('sent from mail\.ru for android', ''),
    ('i hope for your help', ''),
    ('thanks? you very much for your help', ''),
    ('thanks? you very much for the help', ''),
    ('thanks? you very much for your reply', ''),
    ('thanks? you very much for your answer', ''),
    ('thanks? you very much', ''),
    ('thanks? you for your help', ''),
    ('thanks? you for your reply', ''),
    ('thanks? you for your answer', ''),
    ('thanks? you', ''),
    ('thanks? u', ''),
    ('thanks? a lot', ''),
    ('thanks very much for your help', ''),
    ('thanks very much', ''),
    ('best thanks', ''),
    ('many thanks', ''),
    ('thanked', ''),
    # ('thankyou', ''),#
    ('thanks?', ''),
    ('thn?x', ''),
    # ('gracias', ''),#
    ('for their efforts', ''),
    ('for the efforts', ''),
    ('for the attention', ''),
    ('for your attention', ''),
    ('for (your )?understanding', ''),
    ('for your assistance', ''),
    ('for your reply', ''),
    ('for a quick answer', ''),
    ('for quickly processing', ''),
    ('in advance for your help', ''),
    ('in advance', ''),
    ('&amp; nbsp;', ''),
    ('&nbsp;', ''),
    ('generated by cloudfront \(cloudfront\) request id: mnnldjbiuraphafqtdpfufdwikpwjbposa==', ''),
    ('\[cid:.*]', ''),
    ('https://login\.paysafecard\.com/customer-auth/\?client_id=mypinspr&theme=mypins&locale=el_cy&redirect_uri=https%0a%0f%0fmy\.paysafecard\.com%0fmypins-psc%0ftokenexchange\.xhtml', ''),
    ('ladies and gentlemen', ''),
    ('ladies\s?&\s?gentlemen', ''),
    ('origin: mailhttps://go\.microsoft\.com/fwlink/\?linkid=000000 for windows 00', ''),
    ('provenance.+dows', ''),
    ('think before printing', ''),
    ('wrote on', ''),
    ('wrote\\b', ''),
    # ('wrote:', ''),#
    ('subject:', ''),
    ('message:', ''),
    # ('subject:\s+message:', 'message:'),
    ('placeholder image', ''),
    ('date:', ''),
    ('to whom:', ''),
    ('\\bto:', ''),
    # ('from:(\W+\w+)+$', ''),
    ('\\from:', ''),
    ('escribio', ''),
    ('\[https?.+]', ''),
    # ('<\s?https?:.+>', ''),#
    ('<?\s?https?:.+>?', ''),
    ('<\s?https?:.+signature', ''),
    # ('sent from mail for windows', ''),#
    # ('sent from e?mail to windows', ''),#
    # ('sent from the mail app for windows', ''),#
    ('sent from the universal email app for android', ''),
    ('sent from windows email', ''),
    # ('sent from the to windows', ''),#
    ('origin mail for windows', ''),
    ('origin: mail for windows', ''),
    # ('sent from email for windows', ''),#
    ('was sent.+dows', ''),
    ('was sent.+vice', ''),
    ('was sent.+hone', ''),
    ('sent.+dows', ''),
    ('sent.+vice', ''),
    ('sent.+hone', ''),
    ('sent from yahoo mail', ''),
    ('was sent from my huawei', ''),
    ('sent from my huawei', ''),
    ('sent from my', ''),
    # ('huawei', ''),
    ('samsung', ''),
    ('galaxy', ''),
    ('iphone', ''),
    ('ipad', ''),
    ('sent from huawei', ''),
    ('\(first attachment\)', ''),
    ('\(second attachment\)', ''),
    ('wikipedia', ''),
    ('virus\.', ''),
    ('\\bre:', ''),
    ('\\bfwd?:', ''),
    ('message:\s+$', ''),
    ('-{2,}', ''),
    ('_{2,}', ''),
    ('\.+', ' '),
    ('\?+', ''),
    (',\s,', ' '),
    ('\s,\s', ' '),
    ('!*', ''),
    (':+', ' '),
    # (':{2,}', ''),
    ('/{2,}', ''),
    ('\s{2,}', ' '),
    ('\(\)', ''),
    ('\+', ''),
    ('\\band$', ''),
    (',+', ','),
    (',+$', ''),
    ('^\s*and\\b', ''),
    ('^\s?,', ''),
    ('^\s?-', ''),
    ('â€™?', ''),
    ('^\s+', ''),
    ('^>.+[!:\d@,-]*', ''),
    ('^\s?>.+$', ''),
    ('>+', ''),
    ('<+', ''),
    ('\s+$', ''),
    ('\t', ''),
    ('\r', ''),
    ('\n+', ' ')
]

for i in text:
    for old, new in replacements:
        i = re.sub(old, new, str(i))
    clean_text.append(i)

for i in clean_text:
    #Input below the name of the column where you want your clean text to be saved
    column_cell = 'B'
    row_cell = clean_text.index(i) + 1
    source[column_cell+str(row_cell)] = i

#Input below the name of the files that you want your raw + cleaned to be saved in.
#Personally I use the same file.
wb.save("Clean_3_Login_intents_with_latest_script_2.xlsx")

elapsed_time_secs = time.time() - start_time
msg = "Execution took: %s secs (Wall clock time)" % timedelta(seconds=round(elapsed_time_secs))
print(msg)

###############################################################################
