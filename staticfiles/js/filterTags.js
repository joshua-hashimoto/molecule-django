/**
 * based on https://www.w3schools.com/howto/howto_js_filter_lists.asp
 */

const filterTags = () => {
    const input = document.getElementById('tag-filter-input');
    const filter = input.value.toUpperCase();
    const ulElement = document.getElementById("tag-list");
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