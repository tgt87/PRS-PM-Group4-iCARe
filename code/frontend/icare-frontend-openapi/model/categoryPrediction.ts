/**
 * iCARE - An Intelligent Car Budgeting Assistant
 * No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)
 *
 * OpenAPI spec version: 1.0.1
 * 
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */
import { Predictions } from './predictions';

export interface CategoryPrediction { 
    name: CategoryPrediction.NameEnum;
    series?: Array<Predictions>;
}
export namespace CategoryPrediction {
    export type NameEnum = 'Category A' | 'Category B' | 'Category C' | 'Category D' | 'Category E';
    export const NameEnum = {
        A: 'Category A' as NameEnum,
        B: 'Category B' as NameEnum,
        C: 'Category C' as NameEnum,
        D: 'Category D' as NameEnum,
        E: 'Category E' as NameEnum
    };
}