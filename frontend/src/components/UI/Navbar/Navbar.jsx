import React, {useContext} from 'react';
import {Link} from "react-router-dom";
import MyButton from "../button/MyButton";
import cl from "./Navbar.module.css"

const Navbar = () => {

    const logout = () => {
        localStorage.removeItem('auth')
    }

    return (
        <div className={cl.navbar}>
            <div className={cl.navbar__links}>
                <Link className={cl.navbar__link} to="/about">главная</Link>
                <Link className={cl.navbar__link} to="/posts">операции</Link>
            </div>
            <MyButton className={cl.navbar__button} onClick={logout}>
                Выйти
            </MyButton>
        </div>
    );
};

export default Navbar;