"use client";
import HomePageNavbar from "./HomePageNavbar";
import SideBar from "./SideBar";
import React, {useState} from 'react';


function HomePage() {
    const [isSideBarOpen, setIsSideBarOpen] = useState(false);

    const onClickSideBarHandler = () => {
        setIsSideBarOpen(!isSideBarOpen);
    };

    return (
        <div className="relative p-4">
            <HomePageNavbar onClickSideBarHandler={onClickSideBarHandler}/>
            <SideBar isOpen={isSideBarOpen} onClickHandler={onClickSideBarHandler}/>
        </div>
      );
}
export default HomePage