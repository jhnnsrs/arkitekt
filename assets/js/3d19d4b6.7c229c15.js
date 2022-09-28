"use strict";(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[150],{3399:(e,t,a)=>{a.r(t),a.d(t,{contentTitle:()=>i,default:()=>c,frontMatter:()=>n,metadata:()=>o,toc:()=>p});var r=a(7462),s=(a(7294),a(3905));a(1839);const n={sidebar_label:"default",title:"apps.default"},i=void 0,o={unversionedId:"reference/apps/default",id:"reference/apps/default",title:"apps.default",description:"Arkitekt Objects",source:"@site/docs/reference/apps/default.md",sourceDirName:"reference/apps",slug:"/reference/apps/default",permalink:"/arkitekt/docs/reference/apps/default",editUrl:"https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/docs/reference/apps/default.md",tags:[],version:"current",frontMatter:{sidebar_label:"default",title:"apps.default"},sidebar:"tutorialSidebar",previous:{title:"connected",permalink:"/arkitekt/docs/reference/apps/connected"},next:{title:"fakts",permalink:"/arkitekt/docs/reference/apps/fakts"}},p=[{value:"Arkitekt Objects",id:"arkitekt-objects",children:[],level:2}],l={toc:p};function c(e){let{components:t,...a}=e;return(0,s.kt)("wrapper",(0,r.Z)({},l,a,{components:t,mdxType:"MDXLayout"}),(0,s.kt)("h2",{id:"arkitekt-objects"},"Arkitekt Objects"),(0,s.kt)("pre",null,(0,s.kt)("code",{parentName:"pre",className:"language-python"},"class Arkitekt(ConnectedApp)\n")),(0,s.kt)("p",null,"Arkitekt"),(0,s.kt)("p",null,"An app that connected to the services of the arkitekt Api,\nit comes included with the following services:"),(0,s.kt)("ul",null,(0,s.kt)("li",{parentName:"ul"},"Rekuest: A service for that handles requests to the arkitekt Api as well as provides an interface to provide functionality on the arkitekt Api."),(0,s.kt)("li",{parentName:"ul"},"Herre: A service for that handles the authentication and authorization of the user"),(0,s.kt)("li",{parentName:"ul"},"Fakts: A service for that handles the discovery and retrieval of the configuration of the arkitekt Api"),(0,s.kt)("li",{parentName:"ul"},"Mikro: A service for that handles the storage and data of microscopy data")),(0,s.kt)("p",null,"Apps have to be always used within a context manager, this is to ensure that the services are properly closed when the app is no longer needed."),(0,s.kt)("p",null,(0,s.kt)("strong",{parentName:"p"},"Example"),":"),(0,s.kt)("p",null,"  ",">",">",">"," from arkitekt import Arkitekt\n",">",">",">"," app = Arkitekt()\n",">",">",">"," with app:\n",">",">",">","     # Do stuff\n",">",">",">"," # App is closed"))}c.isMDXComponent=!0}}]);