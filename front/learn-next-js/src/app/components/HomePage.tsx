"use client";
import HomePageNavbar from "./HomePageNavbar";
import SideBar from "./SideBar";
import React, {useState} from 'react';


function HomePage() {
    const [isSideBarOpen, setIsSideBarOpen] = useState(false);

    const onClickHandler = () => {
        setIsSideBarOpen(!isSideBarOpen);
    };

    return (
        <div className="relative p-4">
            <HomePageNavbar onClickHandler={onClickHandler}/>
            <SideBar isOpen={isSideBarOpen} onClickHandler={onClickHandler}/>
        </div>
      );
}
export default HomePage