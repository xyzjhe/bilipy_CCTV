var rule = {
    title: '6vFilm',
    host: 'https://www.66s.cc',
    // homeUrl:'/',
	///fyclass/index_fypage.html
    url: '/fyclass/',
    searchUrl: '/?s=**&post_type=post',
    searchable: 0, //�Ƿ�����ȫ������,
    quickSearch: 0, //�Ƿ����ÿ�������,
    filterable: 0, //�Ƿ����÷���ɸѡ,
    headers: { //��վ������ͷ,����֧�����е�,����ua��cookies
        'User-Agent': 'MOBILE_UA',
        // "Cookie": "searchneed=ok"
    },
    // class_name:'��Ӱ&�缯&����',
    // class_url:'movie&airing&anime',
    class_parse: '#menus li.menu-item current_page_item;a&&Text;a&&href;(.*)',
    cate_exclude: '��ҳ|^�ɰ�6v$',
    play_parse: true,
    lazy: 'js:let purl=input.split("|")[0];let referer=input.split("|")[1];let zm=input.split("|")[2];print("purl:"+purl);print("referer:"+referer);print("zm:"+zm);let myua="okhttp/3.15";if(/ddrkey/.test(purl)){let ret=request(purl,{Referer:referer,withHeaders:true,"User-Agent":myua});log(ret);input=purl}else{let html=request(purl,{headers:{Referer:referer,"User-Agent":myua}});print(html);try{input=JSON.parse(html).url||{}}catch(e){input=purl}}',
    limit: 6,
    //�Ƽ�:'.indexShowBox;ul&&li;a&&title;img&&data-src;.s1&&Text;a&&href',
    double: true, // �Ƽ������Ƿ�˫�㶨λ
    һ��: '.mainleft&&thumbnail;a:src&&Text;&&href',
    ����: {
        "title": ".post-title&&Text;.cat-links&&Text",
        "img": ".doulist-item&&img&&data-cfsrc",
        "desc": ".published&&Text",
        "content": ".abstract&&Text",
        "tabs": "js:TABS=['����','����(ò�Ʋ��ܲ���)']",
        lists: 'js:log(TABS);let d=[];pdfh=jsp.pdfh;pdfa=jsp.pdfa;if(typeof play_url==="undefined"){var play_url=""}function getLists(html){let src=pdfh(html,".wp-playlist-script&&Html");src=JSON.parse(src).tracks;let list1=[];let list2=[];src.forEach(function(it){let src0=it.src0;let src1=it.src1;let src2=it.src2;let title=it.caption;let url1="https://ddys.tv/getvddr/video?id="+src1+"&dim=1080P+&type=mix";let url2="https://w.ddys.tv"+src0+"?ddrkey="+src2;let zm="https://ddys.tv/subddr/"+it.subsrc;list1.push({title:title,url:url1,desc:zm});list2.push({title:title,url:url2,desc:zm})});return{list1:list1,list2:list2}}var data=getLists(html);var list1=data.list1;var list2=data.list2;let nums=pdfa(html,"body&&.post-page-numbers");nums.forEach(function(it){let num=pdfh(it,"body&&Text");log(num);let nurl=input+num+"/";if(num==1){return}log(nurl);let html=request(nurl);let data=getLists(html);list1=list1.concat(data.list1);list2=list2.concat(data.list2)});list1=list1.map(function(item){return item.title+"$"+play_url+urlencode(item.url+"|"+input+"|"+item.desc)});list2=list2.map(function(item){return item.title+"$"+play_url+urlencode(item.url+"|"+input+"|"+item.desc)});LISTS=[list1,list2];',
    },
    ����: '#main&&article;.post-title&&Text;;.published&&Text;a&&href',
    �Ƽ�: '*'
}