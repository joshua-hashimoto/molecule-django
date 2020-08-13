/**
 * based on https://www.w3schools.com/howto/howto_js_filter_lists.asp
 */

const filterRelatedArticles = () => {
    const input = document.getElementById('related-article-filter-input');
    const filter = input.value.toUpperCase();
    const ulElement = document.getElementById("related-article-list");
    const liElements = ulElement.getElementsByTagName('li');

    for (const li of liElements) {
        const txtValue = li.textContent || li.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li.style.display = "";
        } else {
            li.style.display = "none";
        }
    }
}