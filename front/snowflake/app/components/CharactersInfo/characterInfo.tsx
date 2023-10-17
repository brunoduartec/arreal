import Image from 'next/image'
import * as fs from 'fs'

interface CharacterInfProp{
    name:string,
    image:string
    description:string
}


interface CharacterLessInfoProp {
    motivations: string[],
    goals:string[],
    conflict:string,
    epiphany:string
}

// function listProperty(props){

// }

function RenderProperty(props) {
    return(<div className='m-3'>
           <b><p>{props.propertyName}</p></b>
                    {props.propertyArray?
                    <ul>
                    {props.propertyArray.map( m => <li>{m}</li>)}
                    </ul>:<p>{props.propertyValue}</p>}
    </div>);
  }


export async function CharacterInfo(prop){

    const fileName = `../../snowflake/step3/${prop.name || "bento"}.json`
    const data:CharacterLessInfoProp = JSON.parse(await fs.readFileSync(fileName));

    console.log("TEXTO", data)
    const imagePath = `/images/characters/${prop.name}.jpg`

    return(
        <div className='flex flex-col bg-gray-500 m-2 rounded-md'>
            <div className='mx-3'>
                <p className='decoration-8 text-transform: uppercase'>{prop.name}</p>
            </div>
            <div className='flex flex-row'>
                <Image
                    src = {imagePath}
                    width={100}
                    height={100}
                    alt={prop.description}
                    className='object-cover object-center rounded-md m-2'
                />
                <div className='flex flex-col'>
                    <div className='flex flex-col'>
                        
                        <RenderProperty
                            propertyName = { "Motivações"}
                            propertyArray  = { data.motivations}
                        />
                        <RenderProperty
                            propertyName = { "Metas"}
                            propertyArray  = { data.goals}
                        />

                        <RenderProperty
                            propertyName = { "Conflito"}
                            propertyValue  = { data.conflict}
                        />

                        <RenderProperty
                            propertyName = { "Epifania"}
                            propertyValue  = { data.epiphany}
                        />


                    </div>
                    
                    <div>
                    <button className="rounded-full  bg-cyan-300 container  w-40">Detalhes</button>
                    </div>
                        
                    

                </div>
            </div>
            
         </div>
    )
}