import { names } from '../../../../../snowflake/step3/characters.json'
import { CharacterInfo } from './characterInfo'

export function  CharactersInfo(prop: any){

    return(<div className='text-black'>
        {names.map((m) =>
        <CharacterInfo
            name = {m}
            image = {m}
        />
        )}
    </div>)
}