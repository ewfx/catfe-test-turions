import { Routes } from '@angular/router';
import { TestGenerationComponent } from '../test-generation/test-generation.component';
import { AppComponent } from './app.component';
import { HomeComponent } from '../home/home.component';

export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'test-generation', component: TestGenerationComponent },
];
