interface BlockInterface {
    name:string,
    shouldRender:boolean
}

export function Block(props: BlockInterface){
    return (<p> {props.shouldRender && `Teste ${props.name}`}</p>)
}