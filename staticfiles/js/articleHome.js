document.addEventListener('DOMContentLoaded', _ => {

    const searchForm = document.getElementById('search-form');

    for (const tag of document.getElementsByClassName('tag')) {
        tag.addEventListener('click', () => {
            const pk = tag.dataset.pk;
            const checkbox = document.querySelector(`input[name="tags"][value="${pk}"]`);
            if (checkbox.checked) {
                checkbox.checked = false;
            } else {
                checkbox.checked = true;
            }
            searchForm.submit();
        });
    }

    for (const check of document.getElementsByName('tags')) {
        check.addEventListener('change', () => {
            searchForm.submit();
        });
    }
});