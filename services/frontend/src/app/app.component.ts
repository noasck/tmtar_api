import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, ParamMap } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  token: string;

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    ) {

  }

  ngOnInit(): void {
  }
}
