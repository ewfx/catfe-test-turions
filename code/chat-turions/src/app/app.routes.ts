import { Routes } from '@angular/router';
import { TestGenerationComponent } from '../test-generation/test-generation.component';
import { AppComponent } from './app.component';
import { HomeComponent } from '../home/home.component';
import { TestUpdateComponent } from '../test-update/test-update.component';
import { TestSuiteComponent } from '../test-suite/test-suite.component';

export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'test-generation', component: TestGenerationComponent },
    { path: 'test-update', component: TestUpdateComponent },
    { path: 'test-suite/:id', component: TestSuiteComponent }
];
