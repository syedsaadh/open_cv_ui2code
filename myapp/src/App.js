import React from 'react';
import ReactDOM from 'react-dom';
import Appbar from 'muicss/lib/react/appbar';
import Button from 'muicss/lib/react/button';
import Container from 'muicss/lib/react/container';
import Input from 'muicss/lib/react/input';
import Radio from 'muicss/lib/react/radio';
import Checkbox from 'muicss/lib/react/checkbox';

import ComponentsPredicted from '../../compoenents_map.json';
import {each} from 'lodash'
import './App.css'
class App extends React.Component {
  card_mapping = (name, props) => {
    switch(name) {
        case 'card simple': {
            return <div className="card card-simple" style={{top: props.top + '%', left: props.left  + '%', position: 'absolute'}}>
                    <div className="heading">
                    Title
                    </div>
                    <div className="desc">
                    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.
                    </div>
                    </div>
        }
        default: 
            return <div className="card card-full" style={{background:'white', top: props.top + '%', left: props.left  + '%', position: 'absolute'}}>
            <div className="heading">
            Title
            </div>
            <div className="desc">
            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.
            </div>
            <div className="actions">
                <Button color="success">ok</Button>
                <Button color="danger">cancel</Button>
            </div>
            </div>
    }
  } 
  icon_mapping = (name) => {
      switch(name) {
            case 'icon shopping': 
                return 'ion-ios-cart'
            case 'icon add':
                return 'ion-plus-round'
            case 'icon arrow left':
                return 'ion-android-arrow-back'
            case 'icon bell':
                return 'ion-ios-bell'
            case 'icon delete':
                return 'ion-trash-a'
            case 'icon hamburger':
                return 'ion-navicon-round'
            case 'icon heart':
                return 'ion-heart'
            case 'icon magnifier':
                return 'ion-android-search'
            case 'icon shopping':
                return 'ion-ios-cart'
            default:
                return 'ion-information-circled'
      }
  }
  mapping = (name, props) => {
    if(name.substring(0, 4) === 'card') {
        return this.card_mapping(name, props)
    }
    if(name.substring(0, 4) === 'icon') {
        const iconname = this.icon_mapping(name)
        return <div style={{top: props.top + '%', left: props.left + '%', position: 'absolute', display: 'inline-block'}}>
                <i style={{color: 'rgb(90, 90, 90)', fontSize: 24, cursor: 'pointer'}} className={iconname}/>
            </div>
    }
    switch (name) {
        case 'toolbar': {
            return <Appbar style={{display: 'flex', padding: '0 16px', justifyContent: 'space-between', alignItems: 'center'}}>
                        <div>
                            <i style={{fontSize: 24, cursor: 'pointer'}} className="ion-navicon-round"/>
                        </div>
                        <div>
                            <Input placeholder="search" />
                        </div>
                        <div>
                        <i style={{fontSize: 24, cursor: 'pointer'}} className="ion-help-circled"/>
                        </div>
                    </Appbar>
        }
        case 'toolbar extended': {
            return <Appbar style={{display: 'flex', background: '#F23F3F', flexDirection: 'column', padding: '0 16px', paddingBottom: '24px'}}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                        <div>
                            <i style={{fontSize: 24, cursor: 'pointer'}} className="ion-navicon-round"/>
                        </div>
                        <div>
                            <Input placeholder="search" />
                        </div>
                        <div>
                        <i style={{fontSize: 24, cursor: 'pointer'}} className="ion-help-circled"/>
                        </div>
                        </div>
                        <h2 style={{paddingLeft: 24, color: 'white'}}>Some text</h2>
                    </Appbar>
        }
        case 'checkbox checked': {
            return <Checkbox name="inputA1" label="Option one" defaultChecked={true} style={{top: props.top + '%', left: props.left  + '%', position: 'absolute'}} />
        }
        case 'checkbox unchecked': {
            return <Checkbox name="inputA1" label="Option one" defaultChecked={false} style={{top: props.top + '%', left: props.left  + '%', position: 'absolute'}} />
        }
        case 'radio checked': {
            return <Radio name="inputA" label="Option two" checked={true} style={{top: props.top + '%', left: props.left  + '%', position: 'absolute'}} />
        }
        case 'radio unchecked': {
            return <Radio name="inputA" label="Option two" checked={false} style={{top: props.top + '%', left: props.left  + '%', position: 'absolute'}} />
        }
        case 'button': { 
            return <Button color="primary" style={{top: props.top + '%', left: props.left  + '%', position: 'absolute'}}>Button</Button>
        }
    }
  }
  renderComp = () => {
      const compRender = []
      each(ComponentsPredicted.components, (item) => {
          if(!item.trulyPredicted)
            return
          const c = this.mapping(item.label, item)
          compRender.push(c)
      })
      return compRender
  }
  render() {
    return (
        <div>
            {
                this.renderComp()
            }
      </div>
    );
  }
}

export default App;
