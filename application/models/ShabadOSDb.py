import sqlite3
import os.path


class ShabadOSDb:
    '''
    to model the http://shabados.org sqllite db
    '''
    _config = None
    _connection = None

    def __init__(self, config):
        if config == None:
            raise TypeError('config not passed in')

        self._config = config

        # don't try catch as we actually want to throw if there's an issue
        db_path = os.path.join(self._config.get('production', 'APPLICATION_PATH'),
                               self._config.get('production', 'db.shabados.path'))

        self._connection = sqlite3.connect(db_path)


    def first_letter_search(self, input):
        """
        First letter search using the gamma field
        @param string the first letter search query
        @return the data
        """

        if input == None:
            raise TypeError('no search string passed in')

        cursor = self._connection.cursor()
        query = "select Verse.ID,Shabad.ShabadID,Verse.Transliteration from Verse join Shabad on Shabad.VerseID = Verse.ID where Verse.FirstLetterEng like ? order by Verse.ID"
        cursor.execute(query, [input + '%'])
        data = cursor.fetchall()
        cursor.close()
        return data

    def get_sabad_by_sabad_id(self, sabad_id):
        """
        get a specific sabad by sabad_id
        @param int the sabad id
        @return the data
        """

        if sabad_id == None:
            raise TypeError('no sabad_id passed in')

        cursor = self._connection.cursor()
        query = "select Verse.ID,Verse.PageNo,Verse.SourceID,Verse.LineNo,Verse.RaagID,Verse.Gurmukhi,Verse.Transliteration,Verse.English from Verse join Shabad on Verse.ID = Shabad.VerseID where Shabad.ShabadID like ?"
        cursor.execute(query, [sabad_id])
        data = cursor.fetchall()
        cursor.close()

        return data
