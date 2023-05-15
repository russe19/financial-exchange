// import PostIdPage from "../pages/PostIdPage";
// import About from "../pages/About";
// import Posts from "../pages/Posts";
// import Error from "../pages/Error";
import Login from "../pages/Login";
import AllCurrency from "../pages/AllCurrency";

export const allRoutes = [
    {path: '/currency', component: <AllCurrency/>, exact: true},
    {path: '/login', component: <Login/>, exact: true},
    // {path: '/register', component: <Register/>, exact: true},
    // {path: '*', component: <Login/>, exact: false},
]