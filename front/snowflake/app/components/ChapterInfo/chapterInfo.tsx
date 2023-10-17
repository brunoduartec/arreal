'use client'

import React, {useState} from 'react'

interface ChapterInfoInterface {
    info:{
        name:string,
        words:number,
        motive:string | string[],
        comment:string | string[],
        characters:string |string[],
        conflicts?:string[],
        status?:string
    }
}


export function  ChapterInfo(prop: ChapterInfoInterface){
    const [isCollapsed, setIsCollapsed] = useState(true);

    const handleClick = () =>{
        setIsCollapsed(!isCollapsed)
    }

    let motives

        const motiveArray = Array.from(prop.info.motive)
        let id=0;
        motives = motiveArray.map( m => <li key={`cpt_${id++}`}>{m}</li>)

    return(
        <div className="container w-100 p-6 max-w-sm mx-auto bg-white rounded-xl shadow-lg flex items-center space-x-4 my-2" onClick={handleClick} >
            <div >
                <div className="text-xl font-medium text-black">{prop.info.name}</div>
                <div className="text-slate-500" hidden={isCollapsed}>{motives}</div>
            </div>
        </div>
);
}