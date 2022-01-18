import pytest
from app import parse_link


class TestParseLink:
    def test_parse_num(self):
        with pytest.raises(Exception):
            parse_link(16)

    def test_parse_string_with_dot(self):
        with pytest.raises(Exception):
            parse_link('I hope not. You might pull a muscle.')

    def test_parse_link_startswith_dot(self):
        with pytest.raises(Exception):
            parse_link('.pytest.org')

    def test_parse_link_endswith_dot(self):
        with pytest.raises(Exception):
            parse_link('docs.pytest.')

    def test_parse_full_link(self):
        assert parse_link('https://habr.com/ru/post/269759/') == 'habr.com'

    def test_parse_short_link(self):
        assert parse_link('docs.pytest.org/en/6.2.x/') == 'docs.pytest.org'

    def test_parse_domain(self):
        assert parse_link('docs.pytest.org') == 'docs.pytest.org'

    def test_parse_extremly_short_link(self):
        assert parse_link('https://a.u/') == 'a.u'

    def test_parse_string_with_dot_looks_like_link(self):
        assert parse_link('Ihopenot.Youmightpullamuscle') == 'Ihopenot.Youmightpullamuscle'

    def test_parse_tricky_domain(self):
        assert parse_link('https.upport') == 'https.upport'

    def test_parse_string(self):
        with pytest.raises(Exception):
            parse_link('She undid the string round the parcel')

    def test_parse_wrong_link(self):
        with pytest.raises(Exception):
            parse_link('http://habr/com/')

    def test_parse_slashes(self):
        with pytest.raises(Exception):
            parse_link('////')

    def test_parse_http_and_slashes(self):
        with pytest.raises(Exception):
            parse_link('http:///')

    def test_parse_https_slashes_and_dots(self):
        with pytest.raises(Exception):
            parse_link('https://../')

    def test_parse_extremly_short_wrong_link(self):
        with pytest.raises(Exception):
            parse_link('https://a/u.ru/')
        
    def test_parse_dobule_protocol_link(self):
        with pytest.raises(Exception):
            parse_link('https://https://docs.pytest')

    def test_parse_link_with_query_string(self):
        assert parse_link('https://ya.ru?q=123') == 'ya.ru'
