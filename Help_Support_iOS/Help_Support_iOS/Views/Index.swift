//
//  Index.swift
//  Help_Support_iOS
//
//  Created by Hongzhe Xie on 1/5/25.
//

import SwiftUI


struct PublishContent: View {
    var body: some View {
        Text("Publish Content")
            .font(.title)
            .padding()
    }
}

struct Activity: View {
    var body: some View {
        Text("Activity")
            .font(.title)
            .padding()
    }
}

struct Account: View {
    var body: some View {
        Text("Account")
            .font(.title)
            .padding()
    }
}


struct Index: View {
    var body: some View {
        TabView {
            ContentView()
                .tabItem {
                    Label("Concent", systemImage: "filemenu.and.selection")
                }

            PublishContent()
                .tabItem {
                    Label("Help", systemImage: "square.and.arrow.up.on.square")
                }

            Activity()
                .tabItem {
                    Label("Activity", systemImage: "archivebox")
                }

            Account()
                .tabItem {
                    Label("Account", systemImage: "person.fill")
                }
        }
    }
}


#Preview {
    Index()
}
