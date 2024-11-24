def softsplit(text,lang):

    """
    This will segment a text string twice, first using SentenceSplitter, and then with additional 
    segmentation for colons, semicolons, and other soft punctuation, such as quotations marks
    that SentenceSplitter will have ignored. The aim is to provide a cleaner and more granular split 
    in order to yield smaller bitexts upon alignment.
    
    Args:
        text - string with text to split
        lang - language code
        
            Language codes include:
            
                Spanish - "es"
                English - "en"
                German - "de"
            
    Returns:
        sents - string with final segmentation

    """
 
    splitter = SentenceSplitter(language=lang)
    sents = splitter.split(text=text)
    sents = [sent.strip() for sent in sents]
    sents = "\n".join(sents)

    # for all languages
    total_cases = re.findall("[:;].{30,1000}\n", sents)
    for item in total_cases:
        if item.count(")") != item.count("("):
            continue
        if item.count("]") != item.count("["):
            continue
        if "https" in sents[sents.index(item)-6:sents.index(item)]:
            continue
        if "i.e." in sents[sents.index(item)-5:sents.index(item)]:
            continue
        if "\n" in sents[sents.index(item)-20:sents.index(item)]:
            continue
        else:
            instance_colon = re.search(re.escape(item),sents).span()[0]
            sents = sents[:instance_colon+1]+"\n"+sents[instance_colon+2:]
    
    # for German
    if lang == "de":
        while re.search("\w[.?!«] [„»]", sents) != None:
            instance_lowcomma = re.search("\w[.?!«] [»„]", sents)
            sents = sents[:instance_lowcomma.span()[0]+2]+"\n"+sents[instance_lowcomma.span()[0]+3:]
            
        total_cases_endquote = re.findall("« [^a-z(]", sents)
        for item in total_cases_endquote:
            instance_endquote = re.search(re.escape(item),sents).span()[0]
            sents = sents[:instance_endquote+1]+"\n"+sents[instance_endquote+2:]
    
    # for Spanish
    if lang == "es":
        while re.search("[.?!»] [—][A-Z¡¿].*\n", sents) != None:
            instance_emdash = re.search("[.?!»] [—][A-Z¡¿].*\n", sents)
            sents = sents[:instance_emdash.span()[0]+1]+"\n"+sents[instance_emdash.span()[0]+2:] 

    sents = re.sub("\n\n","\n",sents)   
                   
    for x in sents.splitlines():
        print(x + "\n")
                   
    return sents