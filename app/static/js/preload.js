const ALLOWED_ROUTES = ["forecast", "hourly", ""];
let route = window.location.href.split("/");
route = route[route.length - 1];
if (route == "") {
  route = "forecast";
}

if (ALLOWED_ROUTES.indexOf(route) >= 0) {
  if (localStorage.getItem("favorites") != undefined) {
    let favorites = JSON.parse(localStorage.getItem("favorites"));
    if (favorites.length > 0) {
      window.location.replace(`/${route}?name=${favorites[0]}`);
    } else {
      window.location.replace(`/${route}`);
    }
  } else {
    window.location.replace(`/${route}`);
  }
}
