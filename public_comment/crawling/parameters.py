arrangement = "Public\?CLASSNAME=PCMMSTDETAIL&id=[0-9]+&Mode=" #検索文字の正規表現

base_url = "https://search.e-gov.go.jp/servlet/Public" #ベースとなるURL

form_paging ={
    "CLASSNAME": "PCMMSTLIST",
    "Page": "0", #ページ番号
    "LastPage": None,
    "Mode": "0",
    "Type": "0",
    "Bunya":None, 
    "Husho:":None,
    "BunyaOpen":None, 
    "HushoOpen":None, 
    "SortOrder":"KoujiDesc",
    "rdoSEARCH4":None, 
    "cmbYERST":None, 
    "txtMonST":None,
    "txtDayST":None, 
    "cmbYERED":None,
    "txtMonED":None,
    "txtDayED":None, 
    "dspcnt": "50",
    "keyword": None,
    "keywordOr": "0",
} #ページングする際に必要になるpostパラメータ

converting={
    "案件番号":"proposal_number",
    "定めようとする命令等の題名":"title",
    "根拠法令項":"ground",
    "行政手続法に基づく手続であるか否か":"low_or_optional",
    "問合せ先（所管府省・部局名等）":"contact", 
    "案の公示日":"announcement_date", 
    "意見・情報受付開始日":"start_accepting", 
    "意見・情報受付締切日":"deadline_date",
}