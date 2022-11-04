import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FormatterService {

  constructor() { }

  capitalizeFirstLetter(str: string) {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }

  formatObjectKey(obj: any) {
    let result: any = {}
    for(let k in obj){
        if(k.includes('_')){
            let splitted = k.split('_')
            let newKey = splitted[0]
            for(let i = 1; i < splitted.length; i++){
                newKey += this.capitalizeFirstLetter(splitted[i])
            }
            result[newKey] = obj[k]
        } else {
            result[k] = obj[k]
        }
    }
    return result
  }

  formatArrayObjectKey(arr: any) {
    let result: any = []
    arr.forEach((obj: any) => {
        result.push(this.formatObjectKey(obj))
    })
    return result
  }

  formatSnakeToCamelCase(str: string) {
    if(!str.includes('_')){
        return str
    }
    let splitted = str.split('_')
    let newString = splitted[0]
    for(let i = 1; i < splitted.length; i++){
        newString += this.capitalizeFirstLetter(splitted[i])
    }
    return newString
  }
}
