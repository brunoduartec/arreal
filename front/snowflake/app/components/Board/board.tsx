import { scene } from '../../../../../snowflake/step6/scenelist.json'

import { ChaptersInfo } from '../ChapterInfo/chaptersInfo';
import { CharactersInfo } from '../CharactersInfo/characters';


export function Board(){
    return(<div className='grid gap-1  grid-cols-2'>
        <div><ChaptersInfo/></div>
        <div className="bg-white">Characters
            <CharactersInfo/>
        </div>
    </div>)
}