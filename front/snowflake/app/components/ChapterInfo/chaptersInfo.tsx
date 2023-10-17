import { scene } from '../../../../../snowflake/step6/scenelist.json'
import { ChapterInfo } from './chapterInfo';


export function ChaptersInfo() {

    const scenes = scene.map(function (m) {
        return m;
    })
    let sceneId = 0;
    const listItems = scenes.map((s, k) => <ChapterInfo
        key={sceneId++}
        info={s}
    />);

    return (
        <div>{listItems}</div>
    );

}