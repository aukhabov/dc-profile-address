import pytest

from extensions import driver_quit
from main_page import MainPage
from profile_page import ProfilePage


@pytest.fixture
def precondition(request):
    main_page = MainPage()
    main_page.authorization()
    profile_page = ProfilePage()

    def postcondition():
        driver_quit()
    request.addfinalizer(postcondition)

    return profile_page


class TestProfileAddress:

    def test_new_manual_address(self, precondition):
        profile_page = precondition
        new_address = profile_page.add_manual_address(f"Кутузовский проспект, 1/7")
        assert new_address in profile_page.address_list()[0], "New address wasn't saved in profile address list"
        profile_page.delete_address(0)

    def test_new_autosuggest_address(self, precondition):
        profile_page = precondition
        suggested_address = profile_page.add_address_from_suggest(f"Ленинградский проспект, 1")
        assert suggested_address in profile_page.address_list()[0], "New address wasn't saved in profile address list"
        profile_page.delete_address(0)

    def test_new_address_from_map(self, precondition):
        profile_page = precondition
        new_address = profile_page.add_address_from_yamap()
        assert new_address in profile_page.address_list()[0], "New address wasn't saved in profile address list"
        profile_page.delete_address(0)

    def test_delete_address(self, precondition):
        profile_page = precondition
        new_address = f"Москва, Комсомольский проспект, 1"
        profile_page.add_manual_address(new_address)
        assert new_address in profile_page.address_list()[0], "New address wasn't saved in profile address list"
        profile_page.delete_address(0)
        profile_page.page_refresh()
        address_list = profile_page.address_list()
        if address_list:
            assert new_address not in address_list[0], "New address wasn't deleted from profile address list"

    @pytest.mark.parametrize("zoom_style", ["in", "out"], ids=["Zoom in", "Zoom out"])
    def test_yamap_zoom(self, precondition, zoom_style):
        profile_page = precondition
        assert profile_page.yamap_zoom(zoom_style), "Zoom button is not clickable on yamap"

    def test_yamap_close(self, precondition):
        profile_page = precondition
        assert profile_page.yamap_close(), "Yamap wasn't close after click on exit button"
