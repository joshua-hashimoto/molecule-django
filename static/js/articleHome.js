document.addEventListener('DOMContentLoaded', _ => {

    const searchForm = document.getElementById('search-form');

    for (const check of document.getElementsByName('tags')) {
        check.addEventListener('change', () => {
            searchForm.submit();
        });
    }
});