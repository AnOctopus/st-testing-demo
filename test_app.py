from streamlit.testing.v1 import AppTest

def get_sorted_colors(at: AppTest):
    """
    Comparing the selected colors is a good heuristic for things changing correctly, so we want it to be easy to get the colors from a script run.
    """
    return [cp.value for cp in at.color_picker]

def test_smoke():
    """Basic smoke test"""
    at = AppTest.from_file("app.py", default_timeout=10).run()
    # Supported elements are primarily exposed as properties on the script
    # results object, which returns a sequence of that element.
    assert not at.exception

def test_palette_size():
    """Changing the palette size will update how many color pickers are shown"""
    at = AppTest.from_file("app.py", default_timeout=10).run()

    # It is easier to find the widget we want by first selecting the
    # sidebar, then querying within that.
    at.sidebar.number_input[0].set_value(2).run()
    
    assert len(at.color_picker) == 2

    # You can also query a widget by key to modify it or check the value
    assert at.number_input(key="sample_size").value == 500
    at.number_input(key="sample_size").set_value(450)

    # For widgets that don't yet have high level interaction methods, we
    # can fall back to the primitive `set_value`.
    at.sidebar.number_input[0].set_value(15).run()
    assert len(at.color_picker) == 15
    assert at.number_input(key="sample_size").value == 450

def test_selected_colors():
    """Changing the source image should change the colors it picks"""
    at = AppTest.from_file("app.py", default_timeout=10).run()
    colors = get_sorted_colors(at)

    # Elements that don't have explicit implementations yet, like `tab`,
    # are still parsed and can be queried using `.get`.
    at.tabs[0].selectbox[0].select("Pretty Night (Leonid Afremov)").run()
    colors2 = get_sorted_colors(at)
    assert colors != colors2

def test_load_url():
    """We can load an image from a URL"""
    at = AppTest.from_file("app.py", default_timeout=10).run()
    colors = get_sorted_colors(at)

    ST_LOGO_URL = "https://user-images.githubusercontent.com/7164864/217935870-c0bc60a3-6fc0-4047-b011-7b4c59488c91.png"
    at.tabs[2].text_input[0].input(ST_LOGO_URL).run()
    assert not at.exception
    colors2 = get_sorted_colors(at)
    assert colors != colors2

def test_seed():
    """Changing the seed will probably change the colors selected"""
    at = AppTest.from_file("app.py", default_timeout=10).run()
    colors = get_sorted_colors(at)

    at.run()
    colors2 = get_sorted_colors(at)
    assert colors == colors2

    at.sidebar.number_input[2].set_value(0).run()
    colors3 = get_sorted_colors(at)
    assert colors != colors3

def test_model():
    """Changing the model will probably change the selected colors."""
    at = AppTest.from_file("app.py", default_timeout=10).run()
    colors_kmeans = get_sorted_colors(at)

    at.sidebar.selectbox[0].select_index(1).run()
    colors_bisect = get_sorted_colors(at)
    assert colors_kmeans != colors_bisect

    # You can also select a value explicitly
    at.sidebar.selectbox[0].select("GaussianMixture").run()
    colors_gaussian = get_sorted_colors(at)
    assert colors_bisect != colors_gaussian

    at.sidebar.selectbox[0].select_index(3).run()
    colors_mini = get_sorted_colors(at)
    assert colors_gaussian != colors_mini
