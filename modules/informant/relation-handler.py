def find_related(key_word):
    """Finds articles in main database (intel, in this case) that contain keyword.
    """
    H(); sprint('This might take a while so please be patient.')
    try:
        keyword = key_word
        found = []
        count = 0
        cycle = 0
        for file in intel.find():
            if ' '+keyword.lower()+' ' in file['payload'][0].lower():
                found.append([file['payload'][0].lower().count(keyword.lower()), file['title']])
                count += file['payload'][0].lower().count(keyword.lower())
                cycle += 1
                if cycle == 1 or cycle == 100000:
                    logging.debug('<<<%s>>>...>' % file['payload'][0].lower().count(keyword.lower()))
                    cycle = 0
    except KeyboardInterrupt:
        logging.warning('User aborted search for keyword "%s".' % key_word)
        H(); sprint("I guess patience isn't your strong suit.")
        controlCentre()
        return

    if found:
        logging.debug('keyword "%s" appears %s times in current universe.' % (key_word, str(count)))
        try:
            found.sort()
            found.reverse()
            for title in found:
                print('%s     (%s)' % (title[1].strip(), str(title[0])))
                time.sleep(0.02)
            controlCentre()
            return
        except KeyboardInterrupt:
            controlCentre()

    else:
        H(); sprint("No mentions of %s exist locally, shall I do an internet sweep for requested data?" % key_word)
        response = input(uzer)
        if 'yes' in response:
            logging.debug('relation seeker sent "%s" to informant.' % key_word)
            H(); sprint('Doing that.')
            informant(key_word, False, 0, False, *['relation seeker'])
        else:
            controlCentre(*[response])
            return