import React, {useContext} from 'react';
import {Route, Routes} from "react-router-dom";
import {allRoutes} from "../router/routes";
import {AuthContext} from "../context";
import Loader from "./UI/Loader/Loader";

const AppRouter = () => {
    // const {isAuth, isLoading} = useContext(AuthContext)
    // console.log(isAuth)

    // if (isLoading) {
    //     return <Loader/>
    // }

    return (
            <div>
                <Routes>
                    {allRoutes.map(route =>
                        <Route
                            path={route.path}
                            element={route.component}
                            exact={route.exact}
                            key={route.path}
                        />
                    )}
                </Routes>
            </div>

    );
};

export default AppRouter;